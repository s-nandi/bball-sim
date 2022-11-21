from typing import TypeVar, List
import pymunk
import pymunk.pygame_util


def limited_velocity_func(max_velocity: float):
    def limit_velocity(body, gravity, damping, d_time):
        pymunk.Body.update_velocity(body, gravity, damping, d_time)
        velocity_length = body.velocity.length
        if velocity_length > max_velocity:
            scale = max_velocity / velocity_length
            body.velocity = body.velocity * scale

    return limit_velocity


T = TypeVar("T")


def rotate(lis: List[T], offset=1) -> List[T]:
    return lis[offset:] + lis[:offset]
