import abc
from typing import Iterator, Optional

from .. import hints, mixins
from ..adapters import socket
from ..bind import Bind
from ..connection import Connection, Session
from ..logger_conf import LOGGER
from ..member import BaseMember
from ..message_package.deserializer import message_deserializer
from ..message_package.message_classes import MessageFromServer
from ..message_package.message_factory import MessageFromFollowerFactory


class IFollower(abc.ABC):

    _socket = socket.ISocket
    is_connected: bool

    @abc.abstractproperty
    def socket(self) -> socket.ISocket:
        pass

    @abc.abstractmethod
    def open_connection(self) -> None:
        pass

    @abc.abstractmethod
    def close_connection(self) -> None:
        pass

    @abc.abstractmethod
    def get_messages(self) -> Iterator[MessageFromServer]:
        pass


class Follower(BaseMember, IFollower, mixins.GracefullyExitMixin):
    def __init__(
        self,
        connection: Connection,
        bind: Bind,
        member_name: Optional[hints.MemberName] = None,
    ):
        super().__init__(member_name=member_name, connection=connection)
        self._message_factory = MessageFromFollowerFactory(sender_member_name=self.member_name, bind=bind)

    @property
    def socket(self) -> socket.BuildInBasedSocket:
        return self._socket

    def open_connection(self) -> None:
        if self.is_connected:
            return

        self._socket = socket.BuildInBasedSocket()
        self.socket.connect(host=self.connection.host, port=self.connection.port)

    def gracefully_exit(self):
        self.close_connection()

    def close_connection(self) -> None:
        if not self.is_connected:
            return
        self.socket.close()
        LOGGER.debug(f'подписчик: "{self.member_name}" был отключен')

    def session(self) -> Session:
        return Session(member_with_persistent_connection=self)

    @property
    def is_connected(self) -> bool:
        return not self.socket.closed

    def _deserialize_message_from_server(self, message_from_server: bytes) -> MessageFromServer:
        return message_deserializer(message_from_server)

    def get_messages(self, auto_ack: bool = False) -> Iterator[MessageFromServer]:
        message_to_get_new_message = self._message_factory.create_give_me_new_message()
        while self.is_connected:
            LOGGER.debug(f'подписчик: {self.member_name} запросил новое сообщение')
            self.socket.send_message(message_to_get_new_message.as_bytes)
            try:
                message = self.socket.recv()
            except OSError:
                continue
            if not message:
                continue

            LOGGER.debug(f'подписчик: {self.member_name} получил новое сообщение')
            message = self._deserialize_message_from_server(message_from_server=message)
            LOGGER.debug('сообщение от сервера было получено')
            if auto_ack:
                self.ack_message(message_from_server=message)
            yield message
        self.close_connection()

    def ack_message(self, message_from_server: MessageFromServer) -> None:
        message = self._message_factory.create_ack_message(message_id=message_from_server.id)
        self.socket.send_message(message.as_bytes)
