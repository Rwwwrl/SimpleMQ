from typing import Union
import socket
import json
import uuid

from connection_config import ConnectionConfig

import logging

logger = logging.getLogger('root')


class IPublisher:
    def __init__(self, connection_config: ConnectionConfig) -> None:
        raise NotImplementedError

    def send_message(self, message: Union[bytes, str]) -> None:
        raise NotImplementedError


class SocketBasedPublisher(IPublisher):
    def __init__(self, connection_config: ConnectionConfig) -> None:
        self._uid = uuid.uuid4()
        self._connection_config = connection_config
        self._sock = socket.socket()
        self._sock.connect((self._connection_config.host, self._connection_config.port))
        logger.debug(f'publisher {self._uid} connected')

    def send_message(self, message: Union[bytes, str]) -> None:
        data = {
            'type': 'publisher',
            'data': message,
        }
        data_as_bytes = json.dumps(data).encode('utf-8')
        self._sock.send(data_as_bytes)
        logger.debug(f'publisher {self._uid} send message')

    def _close_connect(self):
        self._sock.close()
        logger.debug(f'publisher {self._uid} disconnected')
