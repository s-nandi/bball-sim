from __future__ import annotations
import math
from typing import Tuple, Union, TYPE_CHECKING
import pymunk

Point = Tuple[float, float]
Vector = Tuple[float, float]
if TYPE_CHECKING:
    from bball.player import Player
    from bball.ball import Ball
    from bball.court import Hoop

    ObjectWithPosition = Union[Player, Hoop, Point, Ball]

ZERO_VECTOR = (0, 0)
BASE_DIRECTION = (1, 0)

ROUND_DIGITS = 4


def position_of(obj: ObjectWithPosition) -> Point:
    if isinstance(obj, tuple):
        return (obj[0], obj[1])
    return obj.position


def projected_position_of(obj: ObjectWithPosition) -> Point:
    try:
        return sum_of(obj.position, obj.velocity)  # type: ignore
    except AttributeError:
        return position_of(obj)


def coords_to_string(tup: Tuple[float, float]) -> str:
    x_coord = round(tup[0], ROUND_DIGITS)
    y_coord = round(tup[1], ROUND_DIGITS)
    return f"({x_coord}, {y_coord})"


def convert_to_tuple(vec: pymunk.Vec2d) -> Tuple[float, float]:
    return (vec.x, vec.y)


def convert_to_vec2d(point: Tuple[float, float]):
    return pymunk.Vec2d(*point)


def to_radians(degrees: float) -> float:
    return degrees * math.pi / 180


def to_degrees(radians: float) -> float:
    return radians * 180 / math.pi


def normalized_angle(radians: float) -> float:
    while radians < -math.pi:
        radians += 2 * math.pi
    while radians >= math.pi:
        radians -= 2 * math.pi
    assert -math.pi <= radians < math.pi
    return radians


def normalized_angle_degrees(degrees: float) -> float:
    while degrees < -180:
        degrees += 360
    while degrees >= 180:
        degrees -= 360
    assert -180 <= degrees <= 180
    return degrees


def turn_degrees_required(degrees: float, target_degrees: float) -> float:
    return min(
        target_degrees - degrees,
        target_degrees - degrees + 360,
        target_degrees - degrees - 360,
        key=abs,
    )


DEFAULT_EPS = 10**-6


def approx(value_1: float, value_2: float, eps: float = DEFAULT_EPS):
    return abs(value_1 - value_2) < eps


def close_to(point_1: Point, point_2: Point, eps: float = DEFAULT_EPS) -> bool:
    return distance_between(point_1, point_2) <= eps


def distance_between(point_1: Point, point_2: Point) -> float:
    return convert_to_vec2d(point_1).get_distance(convert_to_vec2d(point_2))


def difference_between(point_1: Point, point_2: Point) -> Vector:
    return convert_to_tuple(convert_to_vec2d(point_1) - convert_to_vec2d(point_2))


def sum_of(vector_1: Vector, vector_2: Vector) -> Vector:
    return convert_to_tuple(convert_to_vec2d(vector_1) + convert_to_vec2d(vector_2))


def divide_by(vector: Vector, denominator: float):
    return convert_to_tuple(convert_to_vec2d(vector) / denominator)


def multiply_by(vector: Vector, coefficient: float):
    return convert_to_tuple(convert_to_vec2d(vector) * coefficient)


def interpolate(point_1: Point, point_2: Point, interp: float) -> Point:
    assert 0 <= interp <= 1
    vec_1 = convert_to_vec2d(point_1)
    vec_2 = convert_to_vec2d(point_2)
    vec_res = vec_1.interpolate_to(vec_2, interp)
    return convert_to_tuple(vec_res)


def midpoint_of(point_1: Point, point_2: Point) -> Point:
    return interpolate(point_1, point_2, 0.5)


def vector_angle_degrees(vector: Vector) -> float:
    return normalized_angle_degrees(convert_to_vec2d(vector).angle_degrees)


def vector_length(vector: Vector) -> float:
    return convert_to_vec2d(vector).length


def angle_degrees_to_vector(angle_degrees: float, length: float) -> Vector:
    vec = length * convert_to_vec2d(BASE_DIRECTION).rotated_degrees(angle_degrees)
    return convert_to_tuple(vec)


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def dot_product(vector_1: Vector, vector_2: Vector) -> float:
    return convert_to_vec2d(vector_1).dot(vector_2)


def in_between_of(candidate: Point, extreme_1: Point, extreme_2: Point) -> bool:
    pt_1 = convert_to_vec2d(extreme_1)
    pt_2 = convert_to_vec2d(candidate)
    pt_3 = convert_to_vec2d(extreme_2)
    vec_1 = pt_2 - pt_1
    vec_2 = pt_3 - pt_2
    dot = vec_1.dot(convert_to_tuple(vec_2))
    return dot >= 0
