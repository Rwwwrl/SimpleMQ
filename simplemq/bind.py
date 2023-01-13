from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import hints


class BindTypes(Enum):

    REGEX_BASED = 'REGEX_BASED'
    DIRECT = 'DIRECT'


@dataclass
class Bind:

    route_string: hints.RouteString
    bind_type: BindTypes = BindTypes.DIRECT
