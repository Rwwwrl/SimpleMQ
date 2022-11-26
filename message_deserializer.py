from typing import Union

from .message.message import MessageFromFollower, MessageFromPublisher, MessageFromServer, PossibleSenderTypes
import json


def message_deserializer(message: bytes) -> Union[MessageFromFollower, MessageFromPublisher, MessageFromServer]:
    message_as_json = json.loads(message.decode('utf-8'))

    if message_as_json['sender_type'] == PossibleSenderTypes.FOLLOWER.value:
        return MessageFromFollower(
            sender_unique_name=message_as_json['sender_unique_name'],
            request_type=message_as_json['request_type'],
            message_text=message_as_json['message_text'],
        )

    if message_as_json['sender_type'] == PossibleSenderTypes.PUBLISHER.value:
        return MessageFromPublisher(
            sender_unique_name=message_as_json['sender_unique_name'],
            request_type=message_as_json['request_type'],
            message_text=message_as_json['message_text'],
        )

    if message_as_json['sender_type'] == PossibleSenderTypes.SERVER.value:
        return MessageFromServer(message_text=message_as_json['message_text'], )
