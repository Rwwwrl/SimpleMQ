from .message import (
    MessageFromFollower,
    MessageFromPublisher,
    MessageFromServer,
    PossibleRequestTypesFromFollower,
    PossibleRequestTypesFromPublisher,
)
from ..hints import MemberName, MessageData


class MessageFromFollowerFactory:
    def __init__(self, unique_sender_name: MemberName):
        self._unique_sender_name = unique_sender_name

    def create_send_message(self, message_text: MessageData) -> MessageFromFollower:
        return MessageFromFollower(
            message_text=message_text,
            request_type=PossibleRequestTypesFromFollower.NEW_MESSAGE,
            sender_member_name=self._unique_sender_name,
        )

    def create_ping_to_connect_message(self) -> MessageFromFollower:
        return MessageFromFollower(
            message_text='',
            request_type=PossibleRequestTypesFromFollower.PING_TO_CONNECT,
            sender_member_name=self._unique_sender_name,
        )

    def create_ping_to_disconnect_message(self) -> MessageFromFollower:
        return MessageFromFollower(
            message_text='',
            request_type=PossibleRequestTypesFromFollower.PING_TO_DISCONNECT,
            sender_member_name=self._unique_sender_name,
        )


class MessageFromPublisherFactory:
    def __init__(self, unique_sender_name: MemberName):
        self._unique_sender_name = unique_sender_name

    def create_send_message(self, message_text: MessageData) -> MessageFromPublisher:
        return MessageFromPublisher(
            message_text=message_text,
            request_type=PossibleRequestTypesFromPublisher.NEW_MESSAGE,
            sender_member_name=self._unique_sender_name,
        )


class MessageFromServerFactory:
    @staticmethod
    def create_send_message(message_text: MessageData) -> MessageFromServer:
        return MessageFromServer(message_text=message_text)
