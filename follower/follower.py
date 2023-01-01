import abc
from typing import Iterator, Optional

from ..infrastructure.socket_adapter import socket
from ..hints import MessageData
from ..message.message_factory import MessageFromFollowerFactory
from ..connection_config import ConnectionConfig
from ..message_deserializer import message_deserializer
from ..member import IMember, BaseMember
from ..message.message import BaseMessage, MessageFromServer
from ..logger_conf import logger
from ..hints import MemberName


class IFollower(abc.ABC):

    _socket = socket.ISocket
    is_connected: bool

    @abc.abstractproperty
    def socket(self) -> socket.ISocket:
        pass

    @abc.abstractmethod
    def _deserialize_message_from_server(self, message_from_server: bytes) -> MessageData:
        pass

    @abc.abstractmethod
    def open_connection(self) -> None:
        pass

    @abc.abstractmethod
    def close_connection(self) -> None:
        pass

    @abc.abstractmethod
    def get_messages(self) -> Iterator[BaseMessage]:
        pass


class BaseFollower(BaseMember, IFollower):
    def __init__(self, connection_config: ConnectionConfig, member_name: Optional[MemberName] = None):
        super().__init__(member_name=member_name, connection_config=connection_config)
        self._message_factory = MessageFromFollowerFactory(unique_sender_name=self.member_name)
        self.is_connected = False

    @property
    def socket(self) -> socket.BuildInBasedSocket:
        return self._socket

    def open_connection(self) -> None:
        if self.is_connected:
            return

        self._socket = socket.BuildInBasedSocket()
        self.socket.connect(host=self.connection_config.host, port=self.connection_config.port)
        ping_to_connect_message = self._message_factory.create_ping_to_connect_message()
        self.socket.send_message(ping_to_connect_message.as_bytes)

        self.is_connected = True

    def close_connection(self) -> None:
        self.socket.close()
        self.is_connected = False
        logger.debug(f'подписчик: "{self.member_name}" был отключен')

    def is_connected(self) -> bool:
        return self.has_connected

    def _deserialize_message_from_server(self, message_from_server: bytes) -> MessageFromServer:
        return message_deserializer(message_from_server)

    def get_messages(self) -> Iterator[BaseMessage]:
        while True:
            message = self.socket.recv()
            if not message:
                continue

            message = self._deserialize_message_from_server(message_from_server=message)
            if message:
                logger.debug('сообщение от сервера было получено')
                yield message
