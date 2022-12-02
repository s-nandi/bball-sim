from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from bball.utils import Point


class ThreePointLine(ABC):
    def is_beyond(self, point: Point):
        return not self.contains(point)

    @abstractmethod
    def other_line(self, width: float):
        pass

    @abstractmethod
    def contains(self, _point: Point):
        pass


@dataclass
class RectangleThreePointLine(ThreePointLine):
    x_lo: float
    x_hi: float
    y_lo: float
    y_hi: float

    def __post_init__(self):
        assert self.x_lo <= self.x_hi
        assert self.y_lo <= self.y_hi

    def other_line(self, width):
        assert 0 <= self.x_lo and self.x_hi <= width
        return RectangleThreePointLine(
            width - self.x_hi, width - self.x_lo, self.y_lo, self.y_hi
        )

    def contains(self, point: Point):
        return self.x_lo <= point[0] <= self.x_hi and self.y_lo <= point[1] <= self.y_hi
