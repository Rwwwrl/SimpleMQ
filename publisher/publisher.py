from ..infrastructure.socket_adapter.socket import BuildInBasedSocket
from typing import Optional

from ..bind.bind import Bind
from ..connection.connection import Connection
from ..hints import MessageText, MemberName
from ..member import BaseMember
from ..logger_conf import logger
from ..message.message_factory import MessageFromPublisherFactory


class IPublisher:
    def send_message(self, message_text: MessageText) -> None:
        raise NotImplementedError


class SocketBasedPublisher(IPublisher, BaseMember):
    def __init__(self, connection: Connection, bind: Bind, member_name: Optional[MemberName] = None):
        super().__init__(connection=connection, member_name=member_name)
        self._socket = BuildInBasedSocket()
        self.socket.connect(host=self.connection.host, port=self.connection.port)
        logger.debug(f'издатель: "{self.member_name}" был подключен к брокеру')
        self._message_factory = MessageFromPublisherFactory(sender_member_name=self.member_name, bind=bind)

    @property
    def socket(self):
        return self._socket

    def send_message(self, message_text: MessageText) -> None:
        message = self._message_factory.create_send_message(message_text=message_text)
        self.socket.send_message(message.as_bytes)
        logger.debug(f'издатель: "{self.member_name}: отправил сообщение')
        self._close_connect()

    def _close_connect(self):
        self.socket.close()
        logger.debug(f'издатель: "{self.member_name}" был отключен')
