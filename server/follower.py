from dataclasses import dataclass

from ..hints import MemberName
from asyncio.streams import StreamWriter


@dataclass
class Follower:

    member_name: MemberName
    stream_writer: StreamWriter

    def __hash__(self):
        return hash(self.member_name)
