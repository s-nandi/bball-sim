from dataclasses import dataclass
from bball_server.validator import (
    valid_max_acceleration,
    valid_max_turn_degrees,
    valid_multiplier,
)


@dataclass
class PlayerAttributes:
    max_acceleration: float
    max_turn_degrees: float
    velocity_decay: float

    def __post_init__(self):
        assert valid_max_acceleration(self.max_acceleration)
        assert valid_max_turn_degrees(self.max_turn_degrees)
        assert valid_multiplier(self.velocity_decay)
