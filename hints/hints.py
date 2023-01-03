from typing import NewType, Any, Dict, Deque

MessageText = NewType('MessageText', Any)
MemberName = NewType('MemberName', str)

StreamName = NewType('StreamName', str)

RouteString = NewType('RouteString', str)

Stream = NewType('Stream', Deque)  # TODO пока что он состоит из MessageFromServer
Streams = NewType('Streams', Dict[StreamName, Stream])
