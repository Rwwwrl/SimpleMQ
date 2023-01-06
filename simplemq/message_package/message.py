from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, TYPE_CHECKING, Union

from .. import mixins
from ..utils.static_funcs import dataclass_to_bytes

if TYPE_CHECKING:
    from .. import hints


class PossibleSenderTypes(Enum):

    FOLLOWER = 'follower'
    PUBLISHER = 'publisher'
    SERVER = 'server'
    CURSOR = 'cursor'


class PossibleRequestTypesFromPublisher(Enum):

    NEW_MESSAGE = 'new_message'


class PossibleRequestTypesFromFollower(Enum):

    NEW_MESSAGE = 'new_message'
    GIVE_ME_NEW_MESSAGE = 'give_me_new_message'
    ACK_MESSAGE = 'ack_message'


class PossibleRequestTypesFromServer(Enum):

    NEW_MESSAGE_TO_FOLLOWER = 'new_message_to_follower'


class PossibleRequestTypesFromCursor(Enum):

    CREATE_STREAM = 'create_stream'


RequestTypesFromMember = Union[PossibleRequestTypesFromPublisher, PossibleRequestTypesFromFollower]


@dataclass(kw_only=True)
class IMessage(mixins.ForwardedObject):
    sender_type: PossibleSenderTypes = None
    request_type: RequestTypesFromMember
    message_body: Optional[hints.MessageBody]


@dataclass(kw_only=True)
class IMessageFromMember(IMessage):

    sender_member_name: hints.MemberName
    route_string: hints.RouteString

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromFollower(IMessageFromMember):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.FOLLOWER


@dataclass(kw_only=True)
class MessageFromPublisher(IMessageFromMember):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.PUBLISHER


@dataclass(kw_only=True)
class MessageFromServer(IMessage):

    id: hints.MessageId

    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.SERVER

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromCursor(IMessage):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.CURSOR

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)
