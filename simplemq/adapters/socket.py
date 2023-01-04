import abc
import socket

from .. import hints


class ISocket(abc.ABC):
    @abc.abstractmethod
    def send_message(self, message: bytes) -> None:
        pass

    @abc.abstractmethod
    def recv(self) -> bytes:
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
    '''

    _sock: socket.socket

    def __init__(self):
        self._sock = socket.socket()

    def send_message(self, message: bytes) -> None:
        self._sock.send(message)

    def recv(self) -> bytes:
        return self._sock.recv(1024)

    def connect(self, host: hints.Host, port: hints.Port) -> None:
        self._sock.connect((host, port))

    def close(self) -> None:
        self._sock.close()

    @property
    def closed(self) -> bool:
        return self._sock._closed
