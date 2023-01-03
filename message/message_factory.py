from .message import (
    MessageFromFollower,
    MessageFromPublisher,
    MessageFromServer,
    MessageFromCursor,
    PossibleRequestTypesFromFollower,
    PossibleRequestTypesFromPublisher,
    PossibleRequestTypesFromCursor,
)
from .. import hints
from ..bind.bind import Bind


class MessageFromFollowerFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_text: hints.MessageText) -> MessageFromFollower:
        return MessageFromFollower(
            message_text=message_text,
            request_type=PossibleRequestTypesFromFollower.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )

    def create_give_me_new_message(self) -> MessageFromFollower:
        return MessageFromFollower(
            message_text='',
            request_type=PossibleRequestTypesFromFollower.GIVE_ME_NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromPublisherFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_text: hints.MessageText) -> MessageFromPublisher:
        return MessageFromPublisher(
            message_text=message_text,
            request_type=PossibleRequestTypesFromPublisher.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromServerFactory:
    @staticmethod
    def create_send_message(message_text: hints.MessageText) -> MessageFromServer:
        return MessageFromServer(message_text=message_text)


class MessageFromCursorFactory:
    @staticmethod
    def create_message_to_create_stream(stream_name: hints.StreamName) -> MessageFromCursor:
        return MessageFromCursor(
            message_text=stream_name,
            request_type=PossibleRequestTypesFromCursor.CREATE_STREAM,
        )
