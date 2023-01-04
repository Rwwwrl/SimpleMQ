from typing import Optional

from .. import hints
from ..adapters.socket import BuildInBasedSocket
from ..bind import Bind
from ..connection import Connection
from ..logger_conf import LOGGER
from ..member import BaseMember
from ..message.message_factory import MessageFromPublisherFactory


class IPublisher:
    def send_message(self, message_text: hints.MessageText) -> None:
        raise NotImplementedError


class SocketBasedPublisher(IPublisher, BaseMember):
    def __init__(self, connection: Connection, bind: Bind, member_name: Optional[hints.MemberName] = None):
        super().__init__(connection=connection, member_name=member_name)
        self._message_factory = MessageFromPublisherFactory(sender_member_name=self.member_name, bind=bind)

    def send_message(self, message_text: hints.MessageText) -> None:
        message = self._message_factory.create_send_message(message_text=message_text)
        self.socket = BuildInBasedSocket()
        self.socket.connect(host=self.connection.host, port=self.connection.port)
        self.socket.send_message(message.as_bytes)
        LOGGER.debug(f'издатель: "{self.member_name}: отправил сообщение')
        self.socket.close()
