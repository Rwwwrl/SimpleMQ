import abc
import uuid
from typing import Optional

from .connection import Connection
from .hints import MemberName


class IMember(abc.ABC):

    _member_name: MemberName
    _connection: Connection

    @abc.abstractproperty
    def member_name(self) -> MemberName:
        pass

    @abc.abstractproperty
    def connection(self) -> Connection:
        pass


class BaseMember(IMember):
    def __init__(self, connection: Connection, member_name: Optional[MemberName] = None):
        if not member_name:
            member_name = str(uuid.uuid4())[:8]
        self._member_name = member_name
        self._connection = connection

    @property
    def member_name(self) -> MemberName:
        return self._member_name

    @property
    def connection(self) -> Connection:
        return self._connection
