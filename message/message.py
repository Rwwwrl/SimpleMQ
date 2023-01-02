from dataclasses import dataclass
from enum import Enum
from typing import Union

from ..hints import MessageText, MemberName
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
    GIVE_ME_NEW_MESSAGE = 'give_me_new_message'


PossibleRequestTypes = Union[PossibleRequestTypesFromFollower, PossibleRequestTypesFromPublisher]


@dataclass(kw_only=True)
class BaseMessage:

    sender_type: PossibleSenderTypes = None
    sender_member_name: MemberName
    request_type: PossibleRequestTypes
    message_text: MessageText

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
class MessageFromServer(ForwardedObject):  # TODO надо логически обьяснить почему это не унаследовано от BaseMessage

    message_text: MessageText
    sender_type: PossibleRequestTypes = None

    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.SERVER

    @property
    def as_bytes(self) -> bytes:
        return dataclass_to_bytes(self)


@dataclass(kw_only=True)
class MessageFromPublisher(BaseMessage, ForwardedObject):
    def __post_init__(self):
        self.sender_type: PossibleSenderTypes = PossibleSenderTypes.PUBLISHER