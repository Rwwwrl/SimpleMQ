from __future__ import annotations

import asyncio
from asyncio.base_events import Server as lib_Server
from asyncio.streams import StreamReader, StreamWriter
from collections import deque
from typing import cast

from . import exceptions
from .stream_writer_wrapper import StreamWriterWrapper
from .. import hints
from ..logger_conf import LOGGER
from ..message_package import message as message_module
from ..message_package.convert_request_message_to_server_message import convert_request_message_to_server_message
from ..message_package.deserializer import message_deserializer

STREAMS = hints.Streams({})
PEL = hints.PEL({})


class Server:
    @classmethod
    async def acreate(cls) -> Server:
        self = cls()
        self.HOST = 'localhost'
        self.PORT = 9090

        self.server: lib_Server = await asyncio.start_server(
            client_connected_cb=self._callback_function,
            host=self.HOST,
            port=self.PORT,
            limit=4,
        )
        return self

    async def run_server(self):
        async with self.server:
            LOGGER.debug(f'сервер был запущен на {self.HOST}:{self.PORT}')
            await self.server.serve_forever()

    async def _callback_function(self, reader: StreamReader, writer: StreamWriter):
        while True:

            try:
                try:    # TODO обернуть в ~ def handle_message
                    request_message = (await reader.read(255))
                except ConnectionResetError:
                    break

                if not request_message:
                    break

                try:
                    message = message_deserializer(message=request_message)
                except Exception:
                    LOGGER.exception(
                        f'request_message должен быть унаследован от ForwardedObject, получено: "{request_message}"',
                    )
                    continue

                LOGGER.debug(f'было получено новое сообщение от {type(message).__name__}')

                if message.sender_type == message_module.PossibleSenderTypes.PUBLISHER:
                    message = cast(message_module.MessageFromPublisher, message)
                    message_from_server = convert_request_message_to_server_message(message=message)
                    stream_name = message.route_string
                    STREAMS[stream_name].append(message_from_server)

                if message.sender_type == message_module.PossibleSenderTypes.CURSOR:
                    message = cast(message_module.MessageFromCursor, message)
                    stream_name = message.message_body
                    try:
                        STREAMS[stream_name]
                    except KeyError:
                        STREAMS[stream_name] = deque([])
                        LOGGER.debug(f'был создан новый стрим с наименованием: {stream_name}')

                if message.sender_type == message_module.PossibleSenderTypes.FOLLOWER:
                    message = cast(message_module.MessageFromFollower, message)
                    if message.request_type == message_module.PossibleRequestTypesFromFollower.GIVE_ME_NEW_MESSAGE.value:    # noqa
                        stream_name = message.route_string
                        stream = STREAMS[stream_name]
                        follower = StreamWriterWrapper(member_name=message.sender_member_name, stream_writer=writer)
                        while True:
                            try:
                                new_message = stream.popleft()
                            except IndexError:
                                await asyncio.sleep(0)
                            else:
                                try:
                                    await self._send_message_to_follower(
                                        follower=follower,
                                        message_from_server=new_message,
                                    )
                                    PEL.setdefault(message.sender_member_name, deque([]))
                                    PEL[message.sender_member_name].append(new_message)
                                except Exception as e:
                                    # если нам не удалось доставить сообщение по какой-либо причине,
                                    # то мы возвращаем его обратно в стрим
                                    stream.appendleft(new_message)
                                    LOGGER.error('Неизвестная ошибка')
                                    raise e
                                else:
                                    break
                    if message.request_type == message_module.PossibleRequestTypesFromFollower.ACK_MESSAGE.value:
                        follower_PEL = PEL[message.sender_member_name]
                        message_id_to_delete = message.message_body
                        for message in follower_PEL.copy():
                            if message.id == message_id_to_delete:
                                follower_PEL.remove(message)
                        LOGGER.debug(f'сообщений с id: {message_id_to_delete} было удалено из PEL подписчика')
            except exceptions.ConnectionToFollowerHasLost:
                break

            except Exception as e:
                LOGGER.exception('При обработке запроса произошла ошибка!')
                raise e

        writer.close()

    async def _send_message_to_follower(
        self,
        follower: StreamWriterWrapper,
        message_from_server: message_module.MessageFromServer,
    ) -> None:
        try:
            follower.stream_writer.write(message_from_server.as_bytes)
            await follower.stream_writer.drain()
            LOGGER.debug(f'сообщение к подписчику: "{follower.member_name}" было успешно доставлено')
        except ConnectionResetError:
            LOGGER.warning(f'сразу доставить сообщения подписчику {follower.member_name} не удалось')
            raise exceptions.ConnectionToFollowerHasLost

        except Exception as e:
            LOGGER.exception('Какая-то ошибка!')
            raise e


async def _run_server():

    server = await Server.acreate()
    await server.run_server()


def run_server():
    asyncio.run(_run_server())
