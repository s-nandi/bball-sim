from abc import ABC
import pymunk
from bball_server.utils import ZERO_VECTOR


class PhysicsObject(ABC):
    _mass: float
    _velocity_decay: float
    _position: pymunk.Vec2d
    _orientation_degrees: float
    _velocity: pymunk.Vec2d
    _has_position: bool
    _has_orientation: bool

    def __init__(self, mass: float, velocity_decay: float):
        self._mass = mass
        self._velocity_decay = velocity_decay
        self._position = ZERO_VECTOR
        self._orientation_degrees = 0
        self._velocity = ZERO_VECTOR
        self._has_position = False
        self._has_orientation = False

    @property
    def is_initialized(self):
        return self._has_orientation and self._has_position

    def init_position(self, position: pymunk.Vec2d):
        assert not self._has_position
        self._position = position
        self._has_position = True

    def init_orientation(self, orientation_degrees: float):
        assert not self._has_orientation
        self._orientation_degrees = orientation_degrees
        self._has_orientation = True

    @property
    def position(self):
        assert self.is_initialized
        return self._position

    @property
    def orientation(self):
        assert self.is_initialized
        return self._orientation_degrees

    @property
    def velocity(self):
        assert self.is_initialized
        return self._velocity
