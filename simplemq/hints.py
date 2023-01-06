from typing import Any, Deque, Dict, NewType

from .message_package.message import MessageFromServer

MessageBody = NewType('MessageBody', Any)
MemberName = NewType('MemberName', str)
MessageId = NewType('MessageId', int)

RouteString = NewType('RouteString', str)

StreamName = NewType('StreamName', str)
Stream = NewType('Stream', Deque[MessageFromServer])
Streams = NewType('Streams', Dict[StreamName, Stream])
PEL = NewType('PEL', Dict[MemberName, Deque[MessageFromServer]])

Host = NewType('Host', str)
Port = NewType('Port', int)
