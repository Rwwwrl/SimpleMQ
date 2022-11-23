from typing import Union
import socket
import json

from connection_config import ConnectionConfig


class IPublisher:
    def __init__(self, connection_config: ConnectionConfig) -> None:
        raise NotImplementedError

    def send_message(self, message: Union[bytes, str]) -> None:
        raise NotImplementedError


class SocketBasedPublisher(IPublisher):
    def __init__(self, connection_config: ConnectionConfig) -> None:
        self._connection_config = connection_config
        self._sock = socket.socket()
        self._sock.connect((self._connection_config.host, self._connection_config.port))

    def send_message(self, message: Union[bytes, str]) -> None:
        data = {
            'type': 'publisher',
            'data': message,
        }
        data_as_bytes = json.dumps(data).encode('utf-8')
        self._sock.send(data_as_bytes)

    def _close_connect(self):
        self._sock.close()
