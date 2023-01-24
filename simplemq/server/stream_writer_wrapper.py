from asyncio.streams import StreamWriter
from dataclasses import dataclass

from ..hints import MemberName


@dataclass
class StreamWriterWrapper:

    member_name: MemberName
    stream_writer: StreamWriter

    def __hash__(self):
        return hash(self.member_name)
