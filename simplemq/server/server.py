from __future__ import annotations

import asyncio
import uuid
from asyncio import exceptions as asyncio_exceptions
from asyncio.base_events import Server as lib_Server
from asyncio.streams import StreamReader, StreamWriter

from decouple import config

from . import exceptions
from .dispatcher_by_sender_type import DispatcherBySenderType
from ..logger_conf import LOGGER
from ..message_package.convert_message_to_bytes import END_OF_MESSAGE
from ..message_package.deserializer import message_deserializer


class Server:
    @classmethod
    async def acreate(cls) -> Server:
        self = cls()
        self.HOST = config('SERVER_HOST')
        self.PORT = int(config('SERVER_PORT'))

        self.server: lib_Server = await asyncio.start_server(
            client_connected_cb=self.safety_client_connect_cb,
            host=self.HOST,
            port=self.PORT,
        )
        return self

    async def run_server(self):
        async with self.server:
            LOGGER.debug(f'сервер был запущен на {self.HOST}:{self.PORT}')
            await self.server.serve_forever()

    async def safety_client_connect_cb(self, reader: StreamReader, writer: StreamWriter) -> None:
        try:
            await self.client_connected_cb(reader=reader, writer=writer)
        except Exception:
            LOGGER.exception('Во время коннекта произошла какая-то ошибка!')

    async def client_connected_cb(self, reader: StreamReader, writer: StreamWriter) -> None:
        connection_uid = str(uuid.uuid4())[:8]
        LOGGER.debug(f'Новоe подключение, connection_uid: {connection_uid}')
        while True:
            try:
                try:
                    try:
                        request_message = await reader.readuntil(END_OF_MESSAGE.encode('utf-8'))
                    except asyncio_exceptions.IncompleteReadError as e:
                        request_message = e.partial
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

                handler_cls = DispatcherBySenderType.get_handler(sender_type=message.sender_type)
                await handler_cls().handle_message(message=message, writer=writer)

            except exceptions.ConnectionToFollowerHasLost:
                break

        LOGGER.debug(f'Подключение connection_uid: {connection_uid} было разорвано')
        writer.close()
        await writer.wait_closed()


async def _run_server():

    server = await Server.acreate()
    await server.run_server()


def run_server():
    asyncio.run(_run_server())
