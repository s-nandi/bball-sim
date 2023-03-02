from dataclasses import dataclass
from bball.shot_probability import ShotProbability
from bball.validator import (
    valid_max_velocity,
    valid_max_acceleration,
    valid_max_turn_degrees,
    valid_multiplier,
)


@dataclass
class PlayerAttributes:
    @dataclass
    class Physical:
        mass: float
        size: float
        max_velocity: float
        max_acceleration: float
        max_turn_degrees: float
        velocity_decay: float

        def __post_init__(self):
            assert valid_max_velocity(self.max_velocity)
            assert valid_max_acceleration(self.max_acceleration)
            assert valid_max_turn_degrees(self.max_turn_degrees)
            assert valid_multiplier(self.velocity_decay)

    @dataclass
    class Skill:
        shot_probability: ShotProbability
        shot_velocity: float
        pass_velocity: float

    physical: Physical
    skill: Skill
