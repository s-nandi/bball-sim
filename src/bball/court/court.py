from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING
from bball.utils import position_of, interpolate, interpolation_coefficient, close_to

if TYPE_CHECKING:
    from bball.court.hoop import Hoop
    from bball.utils import Point, ObjectWithPosition


@dataclass
class HalfCourt:
    back: float
    front: float
    left: float
    right: float

    @property
    def width(self) -> float:
        return abs(self.back - self.front)

    @property
    def height(self) -> float:
        return abs(self.left - self.right)

    def position_to_multiplier(self, point: Point) -> Tuple[float, float]:
        x_coeff = interpolation_coefficient(point[0], self.back, self.front)
        y_coeff = interpolation_coefficient(point[1], self.left, self.right)
        multiplier = (x_coeff, y_coeff)
        assert close_to(self.multiplier_to_position(multiplier), point)
        return multiplier

    def multiplier_to_position(self, multiplier: Tuple[float, float]) -> Point:
        x_position = interpolate(self.back, self.front, multiplier[0])
        y_position = interpolate(self.left, self.right, multiplier[1])
        return (x_position, y_position)


class Court:
    _dimensions: Tuple[float, float]
    _hoops: Tuple[Hoop, Hoop]

    def __init__(self, dimensions: Tuple[float, float], hoops: Tuple[Hoop, Hoop]):
        self._dimensions = dimensions
        self._hoops = hoops
        for hoop in self._hoops:
            assert self._contains_position(hoop.position)

    @property
    def dimensions(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def width(self) -> float:
        return self._dimensions[0]

    @property
    def height(self) -> float:
        return self._dimensions[1]

    def hoop(self, index: int) -> Hoop:
        return self._hoops[index]

    def half_court(self, index: int) -> HalfCourt:
        back = 0.0
        front = self.width / 2
        left = 0.0
        right = self.height
        if index == 1:
            back = self.width - back
            left, right = right, left
        return HalfCourt(back=back, front=front, left=left, right=right)

    def is_inbounds(self, obj: ObjectWithPosition) -> bool:
        return self._contains_position(position_of(obj))

    def _contains_position(self, position: Point):
        inbounds = True
        for dimension in range(2):
            inbounds &= 0 <= position[dimension] <= self._dimensions[dimension]
        return inbounds
