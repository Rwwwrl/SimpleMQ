from __future__ import annotations

from typing import TYPE_CHECKING

from ..bind.bind import Bind
from ..message import message_factory
from ..message import message
from ..infrastructure.socket_adapter import socket

if TYPE_CHECKING:
    from .connection import Connection


class Cursor:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.message_factory = message_factory.MessageFromCursorFactory

    def create_stream(self, bind: Bind) -> None:
        message_to_create_new_stream = self.message_factory.create_message_to_create_stream(
            stream_name=bind.route_string,  # TODO пока не бьются наименования, в общем смысле route_key != stream_name
        )
        self._send_message(message_from_cursor=message_to_create_new_stream)

    def _send_message(self, message_from_cursor: message.MessageFromCursor) -> None:
        self.socket = socket.BuildInBasedSocket()
        self.socket.connect(self.connection.host, self.connection.port)
        self.socket.send_message(message_from_cursor.as_bytes())
        self.socket.close()
        del self.socket
