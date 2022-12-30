from dataclasses import dataclass
from enum import Enum
from typing import Union

from ..hints import MessageData, MemberName
from ..mixins.forwarded_object import ForwardedObject
from ..utils.static_funcs.dataclass_to_bytes import dataclass_to_bytes


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
    message_text: MessageData

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromFollower(BaseMessage, ForwardedObject):

    sender_type: PossibleSenderTypes = PossibleSenderTypes.FOLLOWER

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromServer(ForwardedObject):

    sender_type: PossibleSenderTypes = PossibleSenderTypes.SERVER
    message_text: MessageData

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromPublisher(BaseMessage, ForwardedObject):

    sender_type: PossibleSenderTypes = PossibleSenderTypes.PUBLISHER