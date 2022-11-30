from __future__ import annotations
from typing import Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from bball_server.player import Player
    from bball_server.ball import Ball
    from bball_server.court.hoop import Hoop
    from bball_server.utils import Point, ObjectWithPosition


class Court:
    _dimensions: Tuple[float, float]
    _hoops: Tuple[Hoop, Hoop]

    def __init__(self, dimensions: Tuple[float, float], hoops: Tuple[Hoop, Hoop]):
        self._dimensions = dimensions
        self._hoops = hoops
        for hoop in self._hoops:
            assert self._contains_position(hoop.position)

    @property
    def width(self) -> float:
        return self._dimensions[0]

    @property
    def height(self) -> float:
        return self._dimensions[1]

    def hoop(self, index: int) -> Hoop:
        return self._hoops[index]

    def is_inbounds(self, obj: ObjectWithPosition) -> bool:
        return self._contains_position(obj.position)

    def _contains_position(self, position: Point):
        inbounds = True
        for dimension in range(2):
            inbounds &= 0 <= position[dimension] <= self._dimensions[dimension]
        return inbounds
