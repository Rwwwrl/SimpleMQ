import abc


class ForwardedObject(abc.ABC):
    @abc.abstractproperty
    def as_bytes(self) -> bytes:
        pass
