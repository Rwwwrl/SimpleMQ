import json
from typing import Union

from . import message_classes as message_module
from ..bind import Bind, BindTypes

PossibleMessages = Union[message_module.MessageFromCursor, message_module.MessageFromFollower,
                         message_module.MessageFromPublisher, message_module.MessageFromServer]


def message_deserializer(message: bytes) -> PossibleMessages:
    message_as_json = json.loads(message.decode('utf-8'))
    sender_type = message_module.PossibleSenderTypes[message_as_json['sender_type']]

    if sender_type == message_module.PossibleSenderTypes.FOLLOWER:
        request_type = message_as_json['request_type']
        return message_module.MessageFromFollower(
            sender_member_name=message_as_json['sender_member_name'],
            request_type=message_module.PossibleRequestTypesFromFollower[request_type],
            message_body=message_as_json['message_body'],
            bind=Bind(
                route_string=message_as_json['bind']['route_string'],
                bind_type=BindTypes[message_as_json['bind']['bind_type']],
            ),
        )

    if sender_type == message_module.PossibleSenderTypes.PUBLISHER:
        request_type = message_as_json['request_type']
        return message_module.MessageFromPublisher(
            sender_member_name=message_as_json['sender_member_name'],
            request_type=message_module.PossibleRequestTypesFromPublisher[request_type],
            message_body=message_as_json['message_body'],
            bind=Bind(
                route_string=message_as_json['bind']['route_string'],
                bind_type=BindTypes[message_as_json['bind']['bind_type']],
            ),
        )

    if sender_type == message_module.PossibleSenderTypes.SERVER:
        request_type = message_as_json['request_type']
        return message_module.MessageFromServer(
            id=int(message_as_json['id']),
            message_body=message_as_json['message_body'],
            request_type=message_module.PossibleRequestTypesFromServer[request_type],
        )

    if sender_type == message_module.PossibleSenderTypes.CURSOR:
        request_type = message_as_json['request_type']
        return message_module.MessageFromCursor(
            message_body=message_as_json['message_body'],
            request_type=message_module.PossibleRequestTypesFromCursor[request_type],
        )
