import abc
import socket

from .. import hints

BUFF_SIZE = 1024


class ISocket(abc.ABC):
    @abc.abstractmethod
    def send_message(self, message: bytes) -> None:
        pass

    @abc.abstractmethod
    def read(self, n: int) -> bytes:
        pass

    @abc.abstractmethod
    def connect(self, host: hints.Host, port: hints.Port) -> None:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass

    @abc.abstractproperty
    def closed(self) -> bool:
        pass


class BuildInBasedSocket(ISocket):
    '''
    класс адаптер, базированный на встроенной библиотеке socket
    при этом мы используем TCP протокол
    '''

    _sock: socket.socket

    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message: bytes) -> None:
        self._sock.send(message)

    def read(self, n: int = BUFF_SIZE) -> bytes:
        return self._sock.recv(BUFF_SIZE)

    def connect(self, host: hints.Host, port: hints.Port) -> None:
        self._sock.connect((host, port))

    def close(self) -> None:
        self._sock.close()

    @property
    def closed(self) -> bool:
        return self._sock._closed
