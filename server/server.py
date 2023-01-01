from __future__ import annotations

from typing import List
import asyncio
from asyncio.base_events import Server as lib_Server
from asyncio.streams import StreamReader, StreamWriter

from . import exceptions
from .follower import Follower
from ..message_deserializer import message_deserializer
from ..message.message import PossibleSenderTypes, MessageFromServer
from ..request_message_convert_to_server_message import request_message_convert_to_server_message
from ..logger_conf import logger

FOLLOWERS: List[Follower] = []


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
            logger.debug(f'сервер был запущен на {self.HOST}:{self.PORT}')
            await self.server.serve_forever()

    async def _callback_function(self, reader: StreamReader, writer: StreamWriter):
        while True:

            try:
                request_message = (await reader.read(255))
            except ConnectionResetError:
                break

            if not request_message:
                break

            try:
                message = message_deserializer(message=request_message)
            except Exception:
                logger.exception(
                    f'request_message должен быть унаследован от ForwardedObject, получено: "{request_message}"',
                )
                continue

            logger.debug(f'было получено новое сообщение от {type(message).__name__}')

            if message.sender_type == PossibleSenderTypes.FOLLOWER:
                follower = Follower(member_name=message.sender_member_name, stream_writer=writer)
                if not follower in FOLLOWERS:
                    logger.debug(f'новый подписчик: "{follower.member_name}"')
                    FOLLOWERS.append(follower)

            if message.sender_type == PossibleSenderTypes.PUBLISHER:
                message_from_server = request_message_convert_to_server_message(message=message)
                await self._send_message_to_followers(message_from_server=message_from_server)

        writer.close()

    async def _send_message_to_followers(self, message_from_server: MessageFromServer) -> None:
        coros = []
        for follower in FOLLOWERS:
            coro = self._send_message_to_follower(follower=follower, message_from_server=message_from_server)
            coros.append(coro)

        try:
            await asyncio.gather(*coros)
        except exceptions.ConnectionToFollowerHasLost as e:
            # TODO пока что мы просто удаляем подписчика из FOLLOWERS, но надо попробовать другую стратегию
            FOLLOWERS.remove(e.follower)

    async def _send_message_to_follower(self, follower: Follower, message_from_server: MessageFromServer) -> None:
        try:
            follower.stream_writer.write(message_from_server.as_bytes)
            await follower.stream_writer.drain()
            logger.debug(f'сообщение к follower: "{follower.member_name}" было успешно доставлено')
        except ConnectionResetError as e:
            logger.warning(f'сразу доставить сообщения подписчику {follower.member_name} не удалось')
            raise exceptions.ConnectionToFollowerHasLost(follower=follower)

        except Exception as e:
            logger.exception('Какая-то ошибка!')
            raise e


async def _run_server():

    server = await Server.acreate()
    await server.run_server()


def run_server():
    asyncio.run(_run_server())
