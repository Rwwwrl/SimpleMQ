from __future__ import annotations

import abc
import asyncio
from asyncio.streams import StreamWriter
from collections import deque
from typing import Callable

from . import exceptions
from .data import PEL, STREAMS
from .stream_writer_wrapper import StreamWriterWrapper
from ..logger_conf import LOGGER
from ..message_package import convert_request_message_to_server_message
from ..message_package import message as message_module


def get_method_by_request_type(instance: IHandler, request_type: message_module.PossibleRequestType) -> Callable:
    attr = f'handle__{request_type.value.lower()}'
    return getattr(instance, attr)


class IHandler(abc.ABC):
    @abc.abstractmethod
    async def handle_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        pass


class BaseHandler(IHandler):
    async def handle_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        method = get_method_by_request_type(self, message.request_type)
        await method(message, writer)


class HandlerMessagesFromFollower(BaseHandler):
    async def handle__give_me_new_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
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

    async def handle__ack_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        follower_PEL = PEL[message.sender_member_name]
        message_id_to_delete = message.message_body
        for message in follower_PEL.copy():
            if message.id == message_id_to_delete:
                follower_PEL.remove(message)
        LOGGER.debug(f'обработка сообщения с id: {message_id_to_delete} была подтвеждена')

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


class HandlerMessagesFromPublisher(BaseHandler):
    async def handle__new_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        message_from_server = convert_request_message_to_server_message(message=message)
        stream_name = message.route_string
        STREAMS[stream_name].append(message_from_server)


class HandlerMessagesFromCursor(BaseHandler):
    async def handle__create_stream(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        stream_name = message.message_body
        try:
            STREAMS[stream_name]
        except KeyError:
            STREAMS[stream_name] = deque([])
            LOGGER.debug(f'был создан новый стрим с наименованием: {stream_name}')
