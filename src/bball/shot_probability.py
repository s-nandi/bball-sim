from abc import ABC, abstractmethod
from dataclasses import dataclass
from bball.validator import valid_probability
from bball.utils import clamp, interpolate, interpolation_coefficient


class ShotProbability(ABC):
    @abstractmethod
    def __call__(self, shot_distance: float) -> float:
        pass


def checked_probability(probability: float) -> float:
    assert valid_probability(probability)
    return probability


@dataclass
class LinearShotProbability(ShotProbability):
    max_percentage: float
    min_shot_distance: float
    min_percentage: float
    max_shot_distance: float

    def __post_init__(self):
        assert self.min_shot_distance <= self.max_shot_distance
        assert valid_probability(self.max_percentage)
        assert valid_probability(self.min_percentage)

    def __call__(self, shot_distance: float) -> float:
        if shot_distance > self.max_shot_distance:
            return 0.0
        clamped_distance = clamp(
            shot_distance, self.min_shot_distance, self.max_shot_distance
        )
        fraction_from_min_percentage = interpolation_coefficient(
            clamped_distance, self.min_shot_distance, self.max_shot_distance
        )
        return checked_probability(
            interpolate(
                self.max_percentage, self.min_percentage, fraction_from_min_percentage
            )
        )


class GuaranteedShotProbability(ShotProbability):
    def __call__(self, _shot_distance: float) -> float:
        return 1.0
