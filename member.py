import abc
import uuid
from typing import Optional

from .connection_config import ConnectionConfig
from .hints import MemberName


class IMember(abc.ABC):

    _member_name: MemberName
    _connection_config: ConnectionConfig

    @abc.abstractproperty
    def member_name(self) -> MemberName:
        pass

    @abc.abstractproperty
    def connection_config(self) -> MemberName:
        pass


class BaseMember(IMember):
    def __init__(self, connection_config: ConnectionConfig, member_name: Optional[MemberName] = None):
        if not member_name:
            member_name = str(uuid.uuid4())
        self._member_name = member_name
        self._connection_config = connection_config

    @property
    def member_name(self) -> MemberName:
        return self._member_name

    @property
    def connection_config(self) -> MemberName:
        return self._connection_config
