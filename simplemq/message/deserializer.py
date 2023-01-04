from typing import Union

from . import message as message_module
import json

PossibleMessages = Union[message_module.MessageFromCursor, message_module.MessageFromFollower,
                         message_module.MessageFromPublisher, message_module.MessageFromServer, ]


def message_deserializer(message: bytes) -> PossibleMessages:
    message_as_json = json.loads(message.decode('utf-8'))

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.FOLLOWER.value:
        return message_module.MessageFromFollower(
            sender_member_name=message_as_json['sender_member_name'],
            request_type=message_as_json['request_type'],
            message_text=message_as_json['message_text'],
            route_string=message_as_json['route_string'],
        )

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.PUBLISHER.value:
        return message_module.MessageFromPublisher(
            sender_member_name=message_as_json['sender_member_name'],
            request_type=message_as_json['request_type'],
            message_text=message_as_json['message_text'],
            route_string=message_as_json['route_string'],
        )

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.SERVER.value:
        return message_module.MessageFromServer(message_text=message_as_json['message_text'], )

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.CURSOR.value:
        return message_module.MessageFromCursor(
            message_text=message_as_json['message_text'],
            request_type=message_as_json['request_type'],
        )