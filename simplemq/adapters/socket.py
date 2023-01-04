import socket
import abc

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
