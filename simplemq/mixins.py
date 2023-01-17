import abc
import signal


class ForwardedObjectMixin(abc.ABC):
    @abc.abstractproperty
    def as_bytes(self) -> bytes:
        pass


class GracefullyExitMixin(abc.ABC):
    def __init__(self):
        signal.signal(signal.SIGINT, self.gracefully_exit)
        signal.signal(signal.SIGTERM, self.gracefully_exit)

    @abc.abstractmethod
    def gracefully_exit(self):
        pass
