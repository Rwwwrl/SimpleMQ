from dataclasses import dataclass
from enum import Enum
from typing import Union

from ..global_typing import MessageText, MemberName
from ..mixins.forwarded_object import ForwardedObjectMixin
from ..static_funcs.dataclass_to_bytes import dataclass_to_bytes


class PossibleSenderTypes(Enum):

    FOLLOWER = 'follower'
    PUBLISHER = 'publisher'
    SERVER = 'server'


class PossibleRequestTypesFromPublisher(Enum):

    NEW_MESSAGE = 'new message'


class PossibleRequestTypesFromFollower(Enum):

    NEW_MESSAGE = 'new message'
    PING_TO_CONNECT = 'ping to connect'
    PING_TO_DISCONNECT = 'ping to disconnet'


PossibleRequestTypes = Union[PossibleRequestTypesFromFollower, PossibleRequestTypesFromPublisher]


@dataclass
class BaseMessage:

    sender_type: PossibleSenderTypes
    sender_unique_name: MemberName
    request_type: PossibleRequestTypes
    message_text: MessageText

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromFollower(BaseMessage, ForwardedObjectMixin):

    sender_type: PossibleSenderTypes = PossibleSenderTypes.FOLLOWER

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromServer(ForwardedObjectMixin):

    sender_type: PossibleSenderTypes = PossibleSenderTypes.SERVER
    message_text: MessageText

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromPublisher(BaseMessage, ForwardedObjectMixin):

    sender_type: PossibleSenderTypes = PossibleSenderTypes.PUBLISHER