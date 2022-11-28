from typing import Tuple
from dataclasses import dataclass
from bball_server.player import Player


@dataclass
class Hoop:
    x_position: float
    y_position: float

    @property
    def position(self) -> Tuple[float, float]:
        return (self.x_position, self.y_position)


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
            inbounds &= 1 <= position[dimension] <= self._dimensions[dimension]
        return inbounds
