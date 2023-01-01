from ..infrastructure.socket_adapter.socket import BuildInBasedSocket
from typing import Optional

from ..connection_config import ConnectionConfig
from ..hints import MessageData, MemberName
from ..member import BaseMember
from ..logger_conf import logger
from ..message.message_factory import MessageFromPublisherFactory


class IPublisher:
    def send_message(self, message_text: MessageData) -> None:
        raise NotImplementedError


class SocketBasedPublisher(IPublisher, BaseMember):
    def __init__(self, connection_config: ConnectionConfig, member_name: Optional[MemberName] = None):
        super().__init__(connection_config=connection_config, member_name=member_name)
        self._socket = BuildInBasedSocket()
        self.socket.connect(host=self.connection_config.host, port=self.connection_config.port)
        logger.debug(f'издатель: "{self.member_name}" был подключен к брокеру')
        self._message_factory = MessageFromPublisherFactory(unique_sender_name=self.member_name)

    @property
    def socket(self):
        return self._socket

    def send_message(self, message_text: MessageData) -> None:
        message = self._message_factory.create_send_message(message_text=message_text)
        self.socket.send_message(message.as_bytes)
        logger.debug(f'издатель: "{self.member_name}: отправил сообщение')

    def _close_connect(self):
        self.socket.close()
        logger.debug(f'издатель: "{self.member_name}" был отключен')
