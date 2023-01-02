from .message import (
    MessageFromFollower,
    MessageFromPublisher,
    MessageFromServer,
    PossibleRequestTypesFromFollower,
    PossibleRequestTypesFromPublisher,
)
from ..hints import MemberName, MessageText


class MessageFromFollowerFactory:
    def __init__(self, sender_member_name: MemberName):
        self.sender_member_name = sender_member_name

    def create_send_message(self, message_text: MessageText) -> MessageFromFollower:
        return MessageFromFollower(
            message_text=message_text,
            request_type=PossibleRequestTypesFromFollower.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
        )

    def create_give_me_new_message(self) -> MessageFromFollower:
        return MessageFromFollower(
            message_text='',
            request_type=PossibleRequestTypesFromFollower.GIVE_ME_NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
        )


class MessageFromPublisherFactory:
    def __init__(self, sender_member_name: MemberName):
        self.sender_member_name = sender_member_name

    def create_send_message(self, message_text: MessageText) -> MessageFromPublisher:
        return MessageFromPublisher(
            message_text=message_text,
            request_type=PossibleRequestTypesFromPublisher.NEW_MESSAGE,
            sender_member_name=self.sender_member_name,
        )


class MessageFromServerFactory:
    @staticmethod
    def create_send_message(message_text: MessageText) -> MessageFromServer:
        return MessageFromServer(message_text=message_text)
