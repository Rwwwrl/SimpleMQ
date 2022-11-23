import socket
import uuid
import json

from connection_config import ConnectionConfig


class BaseFollower:
    def __init__(self, connection_config: ConnectionConfig):
        self._connection_config = connection_config
        self._uid = uuid.uuid4()
        self._connect()

    def _connect(self) -> None:
        if hasattr(self, '_connected') and self._connected:
            return

        self.sock = socket.socket()
        self.sock.connect((self._connection_config.host, self._connection_config.port))

        ping_message_to_start = json.dumps({'type': 'follower'}).encode('utf-8')
        self.sock.send(ping_message_to_start)

        self._connected = True

    def _close_connect(self) -> None:
        self.sock.close()
        self._connected = False

    def messages(self) -> None:
        while True:
            data = self.sock.recv(1024)
            message = data.decode('utf-8')  # TODO
            yield message

    def __iter__(self):
        return self.messages()


class Follower(BaseFollower):
    pass
