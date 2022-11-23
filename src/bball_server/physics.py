from typing import Tuple
import pymunk
from bball_server.utils import BASE_DIRECTION
from bball_server.validator import valid_angle_degrees


def kinematic_step(
    position: pymunk.Vec2d,
    velocity: pymunk.Vec2d,
    acceleration_orientation_degrees: float,
    acceleration_magnitude: float,
    velocity_decay: float,
) -> Tuple[pymunk.Vec2d, pymunk.Vec2d]:
    direction = BASE_DIRECTION.rotated_degrees(acceleration_orientation_degrees)
    acceleration = direction.scale_to_length(acceleration_magnitude)
    velocity += acceleration
    position += velocity
    velocity *= 1 - velocity_decay
    return position, velocity


def add_angle(angle: float, delta: float) -> float:
    assert valid_angle_degrees(angle)
    assert valid_angle_degrees(delta)
    angle += delta
    if angle < -180:
        angle += 360
    if angle > 180:
        angle -= 360
    assert valid_angle_degrees(angle)
    return angle
