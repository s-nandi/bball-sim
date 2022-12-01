from abc import ABC, abstractmethod
from dataclasses import dataclass
from bball_server.validator import valid_probability
from bball_server.utils import clamp


def interpolate(small: float, big: float, fraction: float) -> float:
    assert 0.0 <= fraction <= 1.0
    assert small <= big
    gap = big - small
    return small + fraction * gap


class ShotProbability(ABC):
    @abstractmethod
    def _probability(self, shot_distance: float) -> float:
        pass

    def probability(self, shot_distance: float) -> float:
        shot_probability = self._probability(shot_distance)
        assert valid_probability(shot_probability)
        return shot_probability


@dataclass
class LinearShotProbability(ShotProbability):
    max_percentage: float
    min_shot_distance: float
    min_percentage: float
    max_shot_distance: float

    def __post_init__(self):
        assert self.min_shot_distance <= self.max_shot_distance

    def _probability(self, shot_distance: float) -> float:
        clamped_distance = clamp(
            shot_distance, self.min_shot_distance, self.max_shot_distance
        )
        fraction_from_min_percentage = (self.max_shot_distance - clamped_distance) / (
            self.max_shot_distance - self.min_shot_distance
        )
        return interpolate(
            self.min_percentage, self.max_percentage, fraction_from_min_percentage
        )


class GuaranteedShotProbability(ShotProbability):
    def _probability(self, _shot_distance: float) -> float:
        return 1.0
