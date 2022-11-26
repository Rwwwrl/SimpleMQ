from typing import Union

from .message.message import MessageFromFollower, MessageFromPublisher, MessageFromServer
from .message.message_factory import MessageFromServerFactory


def request_message_convert_to_server_message(
    message: Union[MessageFromFollower, MessageFromPublisher],
) -> MessageFromServer:
    factory = MessageFromServerFactory
    return factory.create_send_message(message_text=message.message_text)
