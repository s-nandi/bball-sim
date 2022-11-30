from dataclasses import dataclass
from bball_server.player import Player
from bball_server.utils import Point


@dataclass
class _ScoringServer:
    _shot_by: Player
    _shot_at: Point
    _shot_from: Point
