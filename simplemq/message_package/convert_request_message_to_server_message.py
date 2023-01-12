from typing import Union

from .message_classes import MessageFromFollower, MessageFromPublisher, MessageFromServer
from .message_factory import MessageFromServerFactory


def convert_request_message_to_server_message(
    message: Union[MessageFromFollower, MessageFromPublisher],
) -> MessageFromServer:
    factory = MessageFromServerFactory
    return factory.create_send_message(message_body=message.message_body)
