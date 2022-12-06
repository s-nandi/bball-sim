from __future__ import annotations
from dataclasses import dataclass, field
from random import uniform
from bball.create import create_strategy
from bball.utils import clamp
from ga.utils import crossover, mutate

SHOOTING_DISTANCE_RANGE = (0.0, 1.0)
DEFENSIVE_TIGHTNESS_RANGE = (0.0, 1.0)


@dataclass
class RegularParameters:
    shooting_distance: float
    defensive_tightness: float
    width: float
    type: str = field(init=False, default="regular")

    def __post_init__(self):
        assert self.width > 0
        self.shooting_distance = clamp(self.shooting_distance, *SHOOTING_DISTANCE_RANGE)
        self.defensive_tightness = clamp(
            self.defensive_tightness, *DEFENSIVE_TIGHTNESS_RANGE
        )

    @staticmethod
    def generate_random(width: float) -> RegularParameters:
        return RegularParameters(
            uniform(*SHOOTING_DISTANCE_RANGE),
            uniform(*DEFENSIVE_TIGHTNESS_RANGE),
            width,
        )

    def mutate(self, delta: float, p_change: float) -> RegularParameters:
        shooting_distance = mutate(self.shooting_distance, delta, p_change)
        defensive_tightness = mutate(self.defensive_tightness, delta, p_change)
        return RegularParameters(shooting_distance, defensive_tightness, self.width)

    def crossover(self, other: RegularParameters, p_first: float) -> RegularParameters:
        return RegularParameters(
            crossover(self.shooting_distance, other.shooting_distance, p_first),
            crossover(self.defensive_tightness, other.defensive_tightness, p_first),
            self.width,
        )

    def strategy(self):
        return create_strategy(
            self.shooting_distance * self.width, self.defensive_tightness
        )
