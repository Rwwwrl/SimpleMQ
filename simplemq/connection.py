from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

from . import hints
from .adapters import socket
from .message_package import message_factory
from .message_package.message_classes import MessageFromCursor

if TYPE_CHECKING:
    from .member import MemberWithPersistentConnectionProtocol


@dataclass
class ConnectionConfig:

    host: hints.Host
    port: hints.Port


class Connection:

    connection_config: ConnectionConfig

    def __init__(self, connection_config: ConnectionConfig):
        self.connection_config = connection_config

    @property
    def host(self) -> hints.Host:
        return self.connection_config.host

    @property
    def port(self) -> hints.Port:
        return self.connection_config.port

    def cursor(self) -> Cursor:
        return Cursor(connection=self)


class Cursor:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.message_factory = message_factory.MessageFromCursorFactory
        self.socket = socket.BuildInBasedSocket()

    def open_connection(self) -> None:
        self.socket.connect(self.connection.host, self.connection.port)

    def close_connection(self) -> None:
        self.socket.close()

    def session(self) -> Session:
        return Session(member_with_persistent_connection=self)

    def create_stream(self, stream_name: hints.StreamName) -> None:
        message_to_create_new_stream = self.message_factory.create_message_to_create_stream(stream_name=stream_name)
        self.socket.send_message(message_to_create_new_stream.as_bytes)

    def _send_message_and_parse_answer(self, message: MessageFromCursor):
        self.socket.send_message(message.as_bytes)
        answer = self.socket.recv().decode('utf-8')
        return json.loads(answer)['message_body']

    def get_STREAMS(self) -> Dict[hints.StreamName, hints.MessagesFromServerAsJson]:
        message = self.message_factory.create_message_to_get_STREAMS()
        return self._send_message_and_parse_answer(message=message)

    def get_STREAM(self, stream_name: hints.StreamName) -> hints.MessagesFromServerAsJson:
        message = self.message_factory.create_message_to_get_STREAM(stream_name=stream_name)
        return self._send_message_and_parse_answer(message=message)

    def get_PELS(self) -> Dict[hints.FollowerName, hints.MessagesFromServerAsJson]:
        message = self.message_factory.create_message_to_get_PELS()
        return self._send_message_and_parse_answer(message=message)

    def get_PEL(self, follower_name: hints.FollowerName) -> hints.MessagesFromServerAsJson:
        message = self.message_factory.create_message_to_get_PEL(follower_name=follower_name)
        return self._send_message_and_parse_answer(message=message)


class Session:
    def __init__(self, member_with_persistent_connection: MemberWithPersistentConnectionProtocol):
        self.member_with_persistent_connection = member_with_persistent_connection

    def __enter__(self) -> None:
        self.member_with_persistent_connection.open_connection()

    def __exit__(self, *args, **kwargs) -> None:
        self.member_with_persistent_connection.close_connection()
