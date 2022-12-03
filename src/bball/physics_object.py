import pymunk
from bball.utils import (
    to_degrees,
    to_radians,
    BASE_DIRECTION,
    convert_to_vec2d,
    convert_to_tuple,
    Point,
    Vector,
    normalized_angle_degrees,
)
from bball.validator import valid_angle_degrees


def velocity_func_with_decay(velocity_decay: float):
    custom_damping = 1.0 - velocity_decay

    def velocity_func(body, gravity, _damping, delta_time):
        pymunk.Body.update_velocity(body, gravity, custom_damping, delta_time)

    return velocity_func


class PhysicsObject:
    _body: pymunk.Body
    _has_position: bool
    _has_orientation: bool

    def __init__(self, mass: float, velocity_decay: float):
        moment = pymunk.moment_for_circle(mass, 0, 1)
        self._body = pymunk.Body(mass, moment)
        self._body.velocity_func = velocity_func_with_decay(velocity_decay)
        self._has_position = False
        self._has_orientation = False

    @property
    def is_initialized(self):
        return self._has_orientation and self._has_position

    @property
    def position(self) -> Point:
        assert self.is_initialized
        return convert_to_tuple(self._body.position)

    @position.setter
    def position(self, position: Point):
        self._body.position = pymunk.Vec2d(*position)
        self._has_position = True

    @property
    def orientation_degrees(self):
        assert self.is_initialized
        return to_degrees(self._body.angle)

    @orientation_degrees.setter
    def orientation_degrees(self, orientation_degrees: float):
        assert valid_angle_degrees(orientation_degrees)
        self._body.angle = to_radians(orientation_degrees)
        self._has_orientation = True

    @property
    def velocity(self) -> Vector:
        assert self.is_initialized
        return convert_to_tuple(self._body.velocity)

    def turn(self, angle: float, time_step: float) -> None:
        assert self.is_initialized
        self.orientation_degrees = normalized_angle_degrees(
            self.orientation_degrees + to_degrees(angle * time_step)
        )
        self._body.velocity = self._body.velocity.rotated(angle * time_step)

    def accelerate(self, acceleration: float, time_step: float) -> None:
        assert self.is_initialized
        force = acceleration * self._body.mass * convert_to_vec2d(BASE_DIRECTION)
        impulse = force * time_step
        self._body.apply_impulse_at_local_point(impulse)