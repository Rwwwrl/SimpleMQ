from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import hints


class IdGenerator:
    @staticmethod
    def get_new_id() -> hints.MessageId:
        from .. import hints
        return hints.MessageId(int(time.time()))
