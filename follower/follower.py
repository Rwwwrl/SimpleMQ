import abc
from typing import Iterator, Optional

from ..connection.connection import Connection
from ..bind.bind import Bind
from ..infrastructure.socket_adapter import socket
from ..hints import MessageText
from ..message.message_factory import MessageFromFollowerFactory
from ..connection_config import ConnectionConfig
from ..message_deserializer import message_deserializer
from ..member import BaseMember
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
    def _deserialize_message_from_server(self, message_from_server: bytes) -> MessageText:
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
    def __init__(
        self,
        connection: Connection,
        bind: Bind,
        member_name: Optional[MemberName] = None,
    ):
        super().__init__(member_name=member_name, connection=connection)
        self._message_factory = MessageFromFollowerFactory(sender_member_name=self.member_name, bind=bind)
        self.is_connected = False

    @property
    def socket(self) -> socket.BuildInBasedSocket:
        return self._socket

    def open_connection(self) -> None:
        if self.is_connected:
            return

        self._socket = socket.BuildInBasedSocket()
        self.socket.connect(host=self.connection.host, port=self.connection.port)
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
        message_to_get_new_message = self._message_factory.create_give_me_new_message()
        while True:
            logger.debug(f'подписчик: {self.member_name} запросил новое сообщение')
            self.socket.send_message(message_to_get_new_message.as_bytes)
            message = self.socket.recv()
            if not message:
                continue

            logger.debug(f'подписчик: {self.member_name} получил новое сообщение')
            message = self._deserialize_message_from_server(message_from_server=message)
            if message:
                logger.debug('сообщение от сервера было получено')
                yield message
