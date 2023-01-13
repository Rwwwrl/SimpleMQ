from __future__ import annotations

from typing import TYPE_CHECKING

from .message_classes import MessageFromServer
from .message_factory import MessageFromServerFactory

if TYPE_CHECKING:
    from .. import hints


def create_server_message(message_body: hints.MessageBody) -> MessageFromServer:
    factory = MessageFromServerFactory
    return factory.create_send_message(message_body=message_body)
