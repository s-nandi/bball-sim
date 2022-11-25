import math
from typing import Tuple
import pymunk

BASE_DIRECTION = pymunk.Vec2d(1, 0)
ZERO_VECTOR = pymunk.Vec2d(0, 0)


def vector_to_string(vec: Tuple[float, float]) -> str:
    x_coord = round(vec[0], 4)
    y_coord = round(vec[1], 4)
    return f"({x_coord}, {y_coord})"


def convert_to_tuple(vec: pymunk.Vec2d) -> Tuple[float, float]:
    return (vec.x, vec.y)


def to_radians(degrees: float) -> float:
    return degrees * math.pi / 180


def to_degrees(radians: float) -> float:
    return radians * 180 / math.pi
