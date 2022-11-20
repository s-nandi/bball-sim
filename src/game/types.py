from typing import Union, Tuple
import pymunk

ConvertibleToVec2d = Union[Tuple[float, float], pymunk.Vec2d]


def convert_to_vec2d(vec: ConvertibleToVec2d) -> pymunk.Vec2d:
    return pymunk.Vec2d(*vec)
