from bball.shot_probability import (
    ShotProbability,
    LinearShotProbability,
    GuaranteedShotProbability,
)


def create_linear_shot_probability(
    max_percentage: float = 1.0,
    min_shot_distance: float = 0.0,
    min_percentage: float = 0.0,
    max_shot_distance: float = 100.0,
) -> ShotProbability:
    return LinearShotProbability(
        max_percentage, min_shot_distance, min_percentage, max_shot_distance
    )


def create_guaranteed_shot_probability():
    return GuaranteedShotProbability()


DEFAULT_SHOT_PROBABILITY = create_linear_shot_probability()
