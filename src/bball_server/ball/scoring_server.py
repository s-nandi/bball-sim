from bball_server.player import Player
from bball_server.utils import Point


class _ScoringServer:
    _shot_by: Player
    _shot_at: Point
    _shot_from: Point

    def __init__(self, shooter: Player, target: Point, shot_from: Point):
        self._shot_by = shooter
        self._shot_at = target
        self._shot_from = shot_from
