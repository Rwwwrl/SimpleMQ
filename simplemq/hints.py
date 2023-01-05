from typing import Any, Deque, Dict, NewType

MessageBody = NewType('MessageBody', Any)
MemberName = NewType('MemberName', str)

RouteString = NewType('RouteString', str)

StreamName = NewType('StreamName', str)
Stream = NewType('Stream', Deque)    # TODO пока что он состоит из MessageFromServer
Streams = NewType('Streams', Dict[StreamName, Stream])

Host = NewType('Host', str)
Port = NewType('Port', int)
