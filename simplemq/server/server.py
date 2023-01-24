from __future__ import annotations

import asyncio
import uuid
from asyncio import exceptions as asyncio_exceptions
from asyncio.base_events import Server as lib_Server
from asyncio.streams import StreamReader, StreamWriter
from dataclasses import dataclass

import yaml

from . import exceptions
from .dispatcher_by_sender_type import DispatcherBySenderType
from .. import hints
from ..logger_conf import LOGGER
from ..message_package.convert_message_to_bytes import END_OF_MESSAGE
from ..message_package.deserializer import message_deserializer


@dataclass
class ServerConfigurationData:

    host: hints.Host
    port: hints.Port


class Server:
    @classmethod
    async def acreate(cls, server_configuration_data: ServerConfigurationData) -> Server:
        self = cls()

        self.server_configuration_data = server_configuration_data
        self.server: lib_Server = await asyncio.start_server(
            client_connected_cb=self.safety_client_connect_cb,
            host=self.server_configuration_data.host,
            port=self.server_configuration_data.port,
        )
        return self

    async def run_server(self):
        async with self.server:
            LOGGER.debug(
                f'сервер был запущен на {self.server_configuration_data.host}:{self.server_configuration_data.port}',
            )
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


async def _run_server(server_configuration_data: ServerConfigurationData):

    server = await Server.acreate(server_configuration_data=server_configuration_data)
    await server.run_server()


def run_server(settings_yml_filepath: str):
    with open(settings_yml_filepath, "r") as stream:
        conf_data = yaml.safe_load(stream)

    server_configuration_data = ServerConfigurationData(
        host=conf_data['host'],
        port=conf_data['port'],
    )
    try:
        LOGGER.setLevel(conf_data['log_level'])
    except ValueError:
        from logging import getLevelNamesMapping
        LOGGER.warning(
            f'''
            Вы задали неверное значение для "log_level" в yaml файле, укажите одно из этих:
            {list(getLevelNamesMapping().keys())}
            ''',
        )
        LOGGER.setLevel('DEBUG')
    except KeyError:
        LOGGER.info('Вы не задачи значение "log_level" в yaml файле, будет использовано значение по умолчанию (DEBUG)')
        LOGGER.setLevel('DEBUG')

    asyncio.run(_run_server(server_configuration_data))
