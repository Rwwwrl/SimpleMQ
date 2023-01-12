from __future__ import annotations

from typing import TYPE_CHECKING

from . import id_generator, message
from ..bind import Bind

if TYPE_CHECKING:
    from .. import hints


class MessageFromFollowerFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_body: hints.MessageBody) -> message.MessageFromFollower:
        return message.MessageFromFollower(
            message_body=message_body,
            request_type=message.PossibleRequestTypesFromFollower.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )

    def create_give_me_new_message(self) -> message.MessageFromFollower:
        return message.MessageFromFollower(
            message_body=None,
            request_type=message.PossibleRequestTypesFromFollower.GIVE_ME_NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )

    def create_ack_message(self, message_id: hints.MessageId) -> message.MessageFromFollower:
        return message.MessageFromFollower(
            message_body=message_id,
            request_type=message.PossibleRequestTypesFromFollower.ACK_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromPublisherFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_body: hints.MessageBody) -> message.MessageFromPublisher:
        return message.MessageFromPublisher(
            message_body=message_body,
            request_type=message.PossibleRequestTypesFromPublisher.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromServerFactory:
    @staticmethod
    def create_send_message(message_body: hints.MessageBody) -> message.MessageFromServer:
        message_id = id_generator.IdGenerator.get_new_id()
        return message.MessageFromServer(
            id=message_id,
            message_body=message_body,
            request_type=message.PossibleRequestTypesFromServer.NEW_MESSAGE_TO_FOLLOWER,
        )


class MessageFromCursorFactory:
    @staticmethod
    def create_message_to_create_stream(stream_name: hints.StreamName) -> message.MessageFromCursor:
        return message.MessageFromCursor(
            message_body=stream_name,
            request_type=message.PossibleRequestTypesFromCursor.CREATE_STREAM,
        )
