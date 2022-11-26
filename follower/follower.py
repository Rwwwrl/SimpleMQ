import socket
import logging
from typing import Optional, Iterator

from connection_config import ConnectionConfig
from ..member import Member
from ..global_typing import MemberName
from ..message.message_factory import MessageFromFollowerFactory
from ..message.message import MessageFromServer
from ..message_deserializer import message_deserializer

logger = logging.getLogger('root')


class BaseFollower(Member):
    def __init__(self, connection_config: ConnectionConfig, unique_name: Optional[MemberName] = None):
        super().__init__(connection_config=connection_config, unique_name=unique_name)
        self._message_factory = MessageFromFollowerFactory(unique_sender_name=self._unique_name)
        self._connect()

    def _connect(self) -> None:
        if hasattr(self, '_connected') and self._connected:
            return

        self.sock = socket.socket()
        self.sock.connect((self._connection_config.host, self._connection_config.port))

        ping_to_connect_message = self._message_factory.create_ping_to_connect_message()
        self.sock.send(ping_to_connect_message.as_bytes)

        self._connected = True
        logger.debug(f'follower {self._unique_name} connected')

    def _close_connect(self) -> None:
        self.sock.close()
        self._connected = False
        logger.debug(f'follower {self._unique_name} disconnected')

    def messages(self) -> Iterator[MessageFromServer]:
        while True:
            message: bytes = self.sock.recv(1024)
            if not message:
                continue

            message: MessageFromServer = message_deserializer(message=message)
            if message:
                logger.debug('message received')
                yield message


class Follower(BaseFollower):
    pass
