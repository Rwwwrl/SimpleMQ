import json
from typing import Union

from . import message as message_module

PossibleMessages = Union[message_module.MessageFromCursor, message_module.MessageFromFollower,
                         message_module.MessageFromPublisher, message_module.MessageFromServer]


def message_deserializer(message: bytes) -> PossibleMessages:
    message_as_json = json.loads(message.decode('utf-8'))

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.FOLLOWER.value:
        return message_module.MessageFromFollower(
            sender_member_name=message_as_json['sender_member_name'],
            request_type=message_as_json['request_type'],
            message_body=message_as_json['message_body'],
            route_string=message_as_json['route_string'],
        )

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.PUBLISHER.value:
        return message_module.MessageFromPublisher(
            sender_member_name=message_as_json['sender_member_name'],
            request_type=message_as_json['request_type'],
            message_body=message_as_json['message_body'],
            route_string=message_as_json['route_string'],
        )

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.SERVER.value:
        return message_module.MessageFromServer(
            id=int(message_as_json['id']),
            message_body=message_as_json['message_body'],
            request_type=message_as_json['request_type'],
        )

    if message_as_json['sender_type'] == message_module.PossibleSenderTypes.CURSOR.value:
        return message_module.MessageFromCursor(
            message_body=message_as_json['message_body'],
            request_type=message_as_json['request_type'],
        )
