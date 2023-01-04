from dataclasses import dataclass
from enum import Enum
from typing import Union

from .. import hints
from ..mixins import ForwardedObject
from ..utils.static_funcs.dataclass_to_bytes import dataclass_to_bytes


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


class PossibleRequestTypesFromCursor(Enum):

    CREATE_STREAM = 'create_stream'


PossibleRequestTypes = Union[PossibleRequestTypesFromFollower,
                             PossibleRequestTypesFromPublisher]    # TODO почему тут только от двух возможно?


@dataclass(kw_only=True)
class BaseMessage:

    sender_type: PossibleSenderTypes = None
    sender_member_name: hints.MemberName
    request_type: PossibleRequestTypes
    message_text: hints.MessageText
    route_string: hints.RouteString

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromFollower(BaseMessage, ForwardedObject):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.FOLLOWER

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromPublisher(BaseMessage, ForwardedObject):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.PUBLISHER


@dataclass(kw_only=True)
class MessageFromServer(ForwardedObject):    # TODO надо логически обьяснить почему это не унаследовано от BaseMessage

    message_text: hints.MessageText
    sender_type: PossibleRequestTypes = None

    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.SERVER

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromCursor(ForwardedObject):

    message_text: hints.MessageText
    request_type: PossibleRequestTypes
    sender_type: PossibleRequestTypes = None

    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.CURSOR

    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)
