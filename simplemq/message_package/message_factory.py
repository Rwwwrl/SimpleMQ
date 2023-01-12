from __future__ import annotations

from typing import TYPE_CHECKING

from . import id_generator, message_classes
from ..bind import Bind

if TYPE_CHECKING:
    from .. import hints


class MessageFromFollowerFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_body: hints.MessageBody) -> message_classes.MessageFromFollower:
        return message_classes.MessageFromFollower(
            message_body=message_body,
            request_type=message_classes.PossibleRequestTypesFromFollower.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )

    def create_give_me_new_message(self) -> message_classes.MessageFromFollower:
        return message_classes.MessageFromFollower(
            message_body=None,
            request_type=message_classes.PossibleRequestTypesFromFollower.GIVE_ME_NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )

    def create_ack_message(self, message_id: hints.MessageId) -> message_classes.MessageFromFollower:
        return message_classes.MessageFromFollower(
            message_body=message_id,
            request_type=message_classes.PossibleRequestTypesFromFollower.ACK_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromPublisherFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_body: hints.MessageBody) -> message_classes.MessageFromPublisher:
        return message_classes.MessageFromPublisher(
            message_body=message_body,
            request_type=message_classes.PossibleRequestTypesFromPublisher.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromServerFactory:
    @staticmethod
    def create_send_message(message_body: hints.MessageBody) -> message_classes.MessageFromServer:
        message_id = id_generator.IdGenerator.get_new_id()
        return message_classes.MessageFromServer(
            id=message_id,
            message_body=message_body,
            request_type=message_classes.PossibleRequestTypesFromServer.NEW_MESSAGE_TO_FOLLOWER,
        )


class MessageFromCursorFactory:
    @staticmethod
    def create_message_to_create_stream(stream_name: hints.StreamName) -> message_classes.MessageFromCursor:
        return message_classes.MessageFromCursor(
            message_body=stream_name,
            request_type=message_classes.PossibleRequestTypesFromCursor.CREATE_STREAM,
        )
