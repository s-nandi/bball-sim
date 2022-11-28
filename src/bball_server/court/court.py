from __future__ import annotations
from typing import Tuple
from bball_server.player import Player
from bball_server.court.hoop import Hoop


class Court:
    _dimensions: Tuple[float, float]
    _hoops: Tuple[Hoop, Hoop]

    def __init__(self, dimensions: Tuple[float, float], hoops: Tuple[Hoop, Hoop]):
        self._dimensions = dimensions
        self._hoops = hoops
        for hoop in self._hoops:
            assert self._contains_position(hoop.position)

    def is_inbounds(self, player: Player) -> bool:
        return self._contains_position(player.position)

    def _contains_position(self, position: Tuple[float, float]):
        inbounds = True
        for dimension in range(2):
            inbounds &= 0 <= position[dimension] <= self._dimensions[dimension]
        return inbounds
