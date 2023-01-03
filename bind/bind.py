from dataclasses import dataclass

from ..hints import RouteString


@dataclass
class Bind:

    route_string: RouteString
