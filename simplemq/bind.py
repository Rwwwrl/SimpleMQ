from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import hints


@dataclass
class Bind:

    route_string: hints.RouteString
