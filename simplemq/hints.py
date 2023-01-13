from typing import Any, Deque, Dict, NewType

from .message_package.message_classes import MessageFromServer

MessageBody = NewType('MessageBody', Any)
MemberName = NewType('MemberName', str)
FollowerName = NewType('FollowerName', MemberName)
MessageId = NewType('MessageId', int)

RouteString = NewType('RouteString', str)

StreamName = NewType('StreamName', str)
Stream = NewType('Stream', Deque[MessageFromServer])
Streams = NewType('Streams', Dict[StreamName, Stream])
PEL = NewType('PEL', Deque[MessageFromServer])
PELS = NewType('PEL', Dict[MemberName, PEL])

Host = NewType('Host', str)
Port = NewType('Port', int)
