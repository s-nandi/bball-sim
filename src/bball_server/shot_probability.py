from dataclasses import dataclass


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def interpolate(small: float, big: float, fraction: float) -> float:
    assert 0.0 <= fraction <= 1.0
    assert small <= big
    gap = big - small
    return small + fraction * gap


@dataclass
class LinearShotProbability:
    max_percentage: float
    min_shot_distance: float
    min_percentage: float
    max_shot_distance: float

    def __post_init__(self):
        assert self.min_shot_distance <= self.max_shot_distance

    def probability(self, shot_distance: float) -> float:
        clamped_distance = clamp(
            shot_distance, self.min_shot_distance, self.max_shot_distance
        )
        fraction_from_min_percentage = (self.max_shot_distance - clamped_distance) / (
            self.max_shot_distance - self.min_shot_distance
        )
        return interpolate(
            self.min_percentage, self.max_percentage, fraction_from_min_percentage
        )
