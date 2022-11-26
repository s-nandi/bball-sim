import pymunk
from bball_server.utils import to_degrees, to_radians, BASE_DIRECTION


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

    def init_position(self, position: pymunk.Vec2d):
        assert not self._has_position
        self._body.position = position
        self._has_position = True

    def init_orientation(self, orientation_degrees: float):
        assert not self._has_orientation
        self._body.angle = to_radians(orientation_degrees)
        self._has_orientation = True

    @property
    def position(self):
        assert self.is_initialized
        return self._body.position

    @property
    def orientation(self):
        assert self.is_initialized
        return to_degrees(self._body.angle)

    @property
    def velocity(self):
        assert self.is_initialized
        return self._body.velocity

    def turn(self, angle: float, time_step: float) -> None:
        assert self.is_initialized
        self._body.angular_velocity = angle
        self._body.velocity = self._body.velocity.rotated(angle * time_step)

    def accelerate(self, acceleration: float, angle: float, time_step: float) -> None:
        assert self.is_initialized
        force_direction = BASE_DIRECTION.rotated(angle)
        force = acceleration * self._body.mass * force_direction
        impulse = force * time_step
        self._body.apply_impulse_at_world_point(impulse, self._body.position)
