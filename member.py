from typing import Optional
import uuid

from .connection_config import ConnectionConfig

from .global_typing import MemberName


class Member:
    def __init__(self, connection_config: ConnectionConfig, unique_name: Optional[MemberName] = None):
        self._connection_config = connection_config
        if not unique_name:
            self._unique_name = uuid.uuid4()
