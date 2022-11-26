from __future__ import annotations


class PlayerMove:
    _acceleration: float
    _turn_degrees: float
    _was_accelerated: bool
    _was_turned: bool

    def __init__(self):
        self.reset()

    def turn(self, turn_degrees: float):
        assert not self._was_turned
        assert (
            not self._was_accelerated
        ), "Cannot turn after accelerating in the same step"
        self._turn_degrees = turn_degrees
        self._was_turned = True

    def accelerate(self, acceleration: float):
        assert not self._was_accelerated
        self._acceleration = acceleration
        self._was_accelerated = True

    def reset(self):
        self._acceleration = 0
        self._turn_degrees = 0
        self._was_accelerated = False
        self._was_turned = False

    @property
    def acceleration(self) -> float:
        return self._acceleration

    @property
    def turn_degrees(self) -> float:
        return self._turn_degrees
