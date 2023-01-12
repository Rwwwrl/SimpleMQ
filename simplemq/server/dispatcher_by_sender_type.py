from typing import Type

from .request_type_handlers import (
    HandlerMessagesFromCursor,
    HandlerMessagesFromFollower,
    HandlerMessagesFromPublisher,
    IHandler,
)
from ..message_package.message_classes import PossibleSenderTypes


class DispatcherBySenderType:
    @staticmethod
    def get_handler(sender_type: PossibleSenderTypes) -> Type[IHandler]:
        d = {
            PossibleSenderTypes.FOLLOWER: HandlerMessagesFromFollower,
            PossibleSenderTypes.PUBLISHER: HandlerMessagesFromPublisher,
            PossibleSenderTypes.CURSOR: HandlerMessagesFromCursor,
        }
        return d[sender_type]
