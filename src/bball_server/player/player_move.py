from dataclasses import dataclass, field


@dataclass
class PlayerMove:
    _acceleration: float = field(init=False, default=0)
    _turn_degrees: float = field(init=False, default=0)
    _was_accelerated: bool = field(init=False, default=False)
    _was_turned: bool = field(init=False, default=False)

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

    @property
    def acceleration(self) -> float:
        return self._acceleration

    @property
    def turn_degrees(self) -> float:
        return self._turn_degrees
