import time

from .. import hints


class IdGenerator:
    @staticmethod
    def get_new_id() -> hints.MessageId:
        return hints.MessageId(int(time.time()))
