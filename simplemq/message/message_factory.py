from . import message
from .. import hints
from ..bind import Bind


class MessageFromFollowerFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_text: hints.MessageText) -> message.MessageFromFollower:
        return message.MessageFromFollower(
            message_text=message_text,
            request_type=message.PossibleRequestTypesFromFollower.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )

    def create_give_me_new_message(self) -> message.MessageFromFollower:
        return message.MessageFromFollower(
            message_text='',
            request_type=message.PossibleRequestTypesFromFollower.GIVE_ME_NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromPublisherFactory:
    def __init__(self, sender_member_name: hints.MemberName, bind: Bind):
        self.sender_member_name = sender_member_name
        self.route_string = bind.route_string

    def create_send_message(self, message_text: hints.MessageText) -> message.MessageFromPublisher:
        return message.MessageFromPublisher(
            message_text=message_text,
            request_type=message.PossibleRequestTypesFromPublisher.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
            route_string=self.route_string,
        )


class MessageFromServerFactory:
    @staticmethod
    def create_send_message(message_text: hints.MessageText) -> message.MessageFromServer:
        return message.MessageFromServer(message_text=message_text)


class MessageFromCursorFactory:
    @staticmethod
    def create_message_to_create_stream(stream_name: hints.StreamName) -> message.MessageFromCursor:
        return message.MessageFromCursor(
            message_text=stream_name,
            request_type=message.PossibleRequestTypesFromCursor.CREATE_STREAM,
        )
