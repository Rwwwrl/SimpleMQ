from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, TYPE_CHECKING, Union

from .. import mixins
from ..bind import Bind

if TYPE_CHECKING:
    from .. import hints


class PossibleSenderTypes(Enum):

    FOLLOWER = 'FOLLOWER'
    PUBLISHER = 'PUBLISHER'
    SERVER = 'SERVER'
    CURSOR = 'CURSOR'


class PossibleRequestType(Enum):
    # для аннотации
    pass


class PossibleRequestTypesFromPublisher(PossibleRequestType):

    NEW_MESSAGE = 'NEW_MESSAGE'


class PossibleRequestTypesFromFollower(PossibleRequestType):

    NEW_MESSAGE = 'NEW_MESSAGE'
    GIVE_ME_NEW_MESSAGE = 'GIVE_ME_NEW_MESSAGE'
    ACK_MESSAGE = 'ACK_MESSAGE'


class PossibleRequestTypesFromServer(PossibleRequestType):

    NEW_MESSAGE_TO_FOLLOWER = 'NEW_MESSAGE_TO_FOLLOWER'


class PossibleRequestTypesFromCursor(PossibleRequestType):

    CREATE_STREAM = 'CREATE_STREAM'
    GET_STREAM = 'GET_STREAM'
    GET_STREAMS = 'GET_STREAMS'
    GET_PEL = 'GET_PEL'
    GET_PELS = 'GET_PELS'


RequestTypesFromMember = Union[PossibleRequestTypesFromPublisher, PossibleRequestTypesFromFollower]


@dataclass(kw_only=True)
class IMessage(mixins.ForwardedObjectMixin):
    sender_type: PossibleSenderTypes = None
    request_type: RequestTypesFromMember
    message_body: Optional[hints.MessageBody]


@dataclass(kw_only=True)
class IMessageFromMember(IMessage):

    sender_member_name: hints.MemberName
    bind: Bind

    @property
    def as_bytes(self) -> bytes:
        from .convert_message_to_bytes import convert_message_to_bytes
        return convert_message_to_bytes(self)


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
        from .convert_message_to_bytes import convert_message_to_bytes
        return convert_message_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromCursor(IMessage):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.CURSOR

    @property
    def as_bytes(self) -> bytes:
        from .convert_message_to_bytes import convert_message_to_bytes
        return convert_message_to_bytes(self)
