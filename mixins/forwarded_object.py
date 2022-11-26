class ForwardedObjectMixin:
    @property
    def as_bytes(self) -> bytes:
        raise NotImplementedError
