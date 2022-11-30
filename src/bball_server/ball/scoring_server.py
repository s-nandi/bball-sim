from dataclasses import dataclass
from bball_server.player import Player
from bball_server.utils import Point


@dataclass
class _ScoringServer:
    shooter: Player
    target: Point
    location: Point
