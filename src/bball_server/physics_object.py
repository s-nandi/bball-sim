from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import pymunk
from bball_server.utils import ZERO_VECTOR


@dataclass
class PhysicsObject(ABC):
    _velocity_decay: float
    _position: pymunk.Vec2d = field(init=False, default=ZERO_VECTOR)
    _orientation_degrees: float = field(init=False, default=0)
    _velocity: pymunk.Vec2d = field(init=False, default=ZERO_VECTOR)
    _has_position: bool = field(init=False, default=False)
    _has_orientation: bool = field(init=False, default=False)

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

    @abstractmethod
    def step(self):
        pass
