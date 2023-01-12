from __future__ import annotations

import asyncio
import uuid
from asyncio.base_events import Server as lib_Server
from asyncio.streams import StreamReader, StreamWriter

from decouple import config

from . import exceptions
from .dispatcher_by_sender_type import DispatcherBySenderType
from ..logger_conf import LOGGER
from ..message_package.deserializer import message_deserializer


class Server:
    @classmethod
    async def acreate(cls) -> Server:
        self = cls()
        self.HOST = config('SERVER_HOST')
        self.PORT = int(config('SERVER_PORT'))

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
        connection_uid = str(uuid.uuid4())[:8]
        LOGGER.debug(f'Новой подключение, connection_uid: {connection_uid}')
        while True:
            try:
                try:
                    request_message = await reader.read(200)
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

            except Exception as e:
                LOGGER.exception('При обработке запроса произошла ошибка!')
                raise e

        LOGGER.debug(f'Подлючение connection_uid: {connection_uid} было разорвано')
        writer.close()
        await writer.wait_closed()


async def _run_server():

    server = await Server.acreate()
    await server.run_server()


def run_server():
    asyncio.run(_run_server())
