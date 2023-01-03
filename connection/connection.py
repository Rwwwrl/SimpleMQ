from ..connection_config import ConnectionConfig
from .cursor import Cursor


class Connection:

    connection_config: ConnectionConfig

    def __init__(self, connection_config: ConnectionConfig):
        self.connection_config = connection_config

    @property
    def host(self) -> str:
        return self.connection_config.host

    @property
    def port(self) -> int:
        return self.connection_config.port

    def cursor(self) -> Cursor:
        return Cursor(connection=self)