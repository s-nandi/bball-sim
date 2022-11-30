import math
from typing import Tuple, Union, TYPE_CHECKING
import pymunk

Point = Tuple[float, float]
Vector = Tuple[float, float]
if TYPE_CHECKING:
    from bball_server.player import Player
    from bball_server.ball import Ball

    ObjectWithPosition = Union[Player, Ball]

BASE_DIRECTION = pymunk.Vec2d(1, 0)
ZERO_VECTOR = pymunk.Vec2d(0, 0)


def coords_to_string(tup: Tuple[float, float]) -> str:
    x_coord = round(tup[0], 4)
    y_coord = round(tup[1], 4)
    return f"({x_coord}, {y_coord})"


def convert_to_tuple(vec: pymunk.Vec2d) -> Tuple[float, float]:
    return (vec.x, vec.y)


def to_radians(degrees: float) -> float:
    return degrees * math.pi / 180


def to_degrees(radians: float) -> float:
    return radians * 180 / math.pi


DEFAULT_EPS = 10**-6


def approx(value_1: float, value_2: float, eps: float = DEFAULT_EPS):
    return abs(value_1 - value_2) < eps


def close_to(
    vec_1: Tuple[float, float], vec_2: Tuple[float, float], eps: float = DEFAULT_EPS
) -> bool:
    delta_x = vec_1[0] - vec_2[0]
    delta_y = vec_1[1] - vec_2[1]
    return approx(delta_x, 0, eps) and approx(delta_y, 0, eps)
