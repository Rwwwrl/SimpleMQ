import socket
from typing import Optional

from ..connection_config import ConnectionConfig
from ..global_typing import MessageText, MemberName
from ..member import Member

from ..message.message_factory import MessageFromPublisherFactory

import logging

logger = logging.getLogger('root')


class IPublisher:
    def send_message(self, message_text: MessageText) -> None:
        raise NotImplementedError


class SocketBasedPublisher(IPublisher, Member):
    def __init__(self, connection_config: ConnectionConfig, unique_name: Optional[MemberName] = None):
        super().__init__(connection_config=connection_config, unique_name=unique_name)
        self._sock = socket.socket()
        self._sock.connect((self._connection_config.host, self._connection_config.port))
        logger.debug(f'publisher {self._unique_name} connected')
        self._message_factory = MessageFromPublisherFactory(unique_sender_name=self._unique_name)

    def send_message(self, message_text: MessageText) -> None:
        message = self._message_factory.create_send_message(message_text=message_text)
        self._sock.send(message.as_bytes)
        logger.debug(f'publisher {self._unique_name} send message')

    def _close_connect(self):
        self._sock.close()
        logger.debug(f'publisher {self._unique_name} disconnected')
