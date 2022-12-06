from __future__ import annotations
from dataclasses import dataclass, field
from random import uniform, choice
from bball.create import created_spaced_strategy
from bball.utils import clamp
from ga.utils import crossover, mutate

SPACING_DISTANCE_RANGE = (0.0, 1.0)
SHOT_QUALITY_RANGE = (0.0, 3.0)
PASS_PROBABILITY_RANGE = (0.0, 1.0)
DEFENSIVE_TIGHTNESS_RANGE = (0.0, 1.0)


@dataclass
class SpacedParameters:
    spacing_distance: float
    shot_quality_threshold: float
    pass_probability: float
    dive_to_basket: bool
    defensive_tightness: float
    width: float
    type: str = field(init=False, default="spaced")

    def __post_init__(self):
        assert self.width > 0
        self.spacing_distance = clamp(self.spacing_distance, *SPACING_DISTANCE_RANGE)
        self.shot_quality_threshold = clamp(
            self.shot_quality_threshold, *SHOT_QUALITY_RANGE
        )
        self.pass_probability = clamp(self.pass_probability, *PASS_PROBABILITY_RANGE)
        self.defensive_tightness = clamp(
            self.defensive_tightness, *DEFENSIVE_TIGHTNESS_RANGE
        )

        self.spacing_distance *= self.width
        self.spacing_distance = clamp(self.spacing_distance, 0, self.width)

    @staticmethod
    def generate_random(width: float) -> SpacedParameters:
        return SpacedParameters(
            uniform(*SPACING_DISTANCE_RANGE),
            uniform(*SHOT_QUALITY_RANGE),
            uniform(*PASS_PROBABILITY_RANGE),
            choice([True, False]),
            uniform(*DEFENSIVE_TIGHTNESS_RANGE),
            width,
        )

    def mutate(self, delta: float, p_change: float) -> SpacedParameters:
        spacing_distance = mutate(self.spacing_distance, delta, p_change)
        shot_quality_threshold = mutate(self.shot_quality_threshold, delta, p_change)
        pass_probability = mutate(self.pass_probability, delta, p_change)
        dive_to_basket = mutate(self.dive_to_basket, True, p_change)
        defensive_tightness = mutate(self.defensive_tightness, delta, p_change)
        return SpacedParameters(
            spacing_distance,
            shot_quality_threshold,
            pass_probability,
            dive_to_basket,
            defensive_tightness,
            self.width,
        )

    def crossover(self, other: SpacedParameters, p_first: float) -> SpacedParameters:
        return SpacedParameters(
            crossover(self.spacing_distance, other.spacing_distance, p_first),
            crossover(
                self.shot_quality_threshold, other.shot_quality_threshold, p_first
            ),
            crossover(self.pass_probability, other.pass_probability, p_first),
            crossover(self.dive_to_basket, other.dive_to_basket, p_first),
            crossover(self.defensive_tightness, other.defensive_tightness, p_first),
            self.width,
        )

    def strategy(self):
        return created_spaced_strategy(
            self.spacing_distance,
            self.shot_quality_threshold,
            self.pass_probability,
            self.dive_to_basket,
            self.defensive_tightness,
        )
