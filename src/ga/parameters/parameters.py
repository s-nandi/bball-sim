from __future__ import annotations
from copy import deepcopy
from typing import Union, TYPE_CHECKING
from runner import run_headless
from ga.parameters.regular_parameters import RegularParameters
from ga.parameters.spaced_parameters import SpacedParameters

if TYPE_CHECKING:
    from bball import Game

Parameters = Union[RegularParameters, SpacedParameters]


def combine(
    parameters_1: Parameters, parameters_2: Parameters, probability: float
) -> Parameters:
    regular_2 = isinstance(parameters_2, RegularParameters)

    if isinstance(parameters_1, RegularParameters) and isinstance(
        parameters_2, RegularParameters
    ):
        return parameters_1.crossover(parameters_2, probability)

    if isinstance(parameters_1, SpacedParameters) and isinstance(
        parameters_2, SpacedParameters
    ):
        return parameters_1.crossover(parameters_2, probability)

    if regular_2:
        parameters_1, parameters_2 = parameters_2, parameters_1

    assert isinstance(parameters_1, RegularParameters)
    assert isinstance(parameters_2, SpacedParameters)
    return parameters_1.crossover(
        RegularParameters(
            parameters_2.spacing_distance,
            parameters_2.defensive_tightness,
            parameters_2.width,
        ),
        probability,
    )


def compare(
    game: Game,
    parameters_1: Parameters,
    parameters_2: Parameters,
    *,
    duration: float,
    fps: int,
    speed_scale: float = 1.0,
) -> bool:
    indexed_strategies = [
        (0, parameters_1.strategy()),
        (1, parameters_2.strategy()),
    ]
    periods = 2
    total_scores = [0.0, 0.0]
    for _ in range(periods):
        game_copy = deepcopy(game)
        for team_index, indexed_strategy in enumerate(indexed_strategies):
            total_scores[indexed_strategy[0]] -= game_copy.scoreboard.score[team_index]
            game_copy.assign_team_strategy(team_index, indexed_strategy[1])

        scoreboard = run_headless(
            game_copy, fps, speed_scale, duration / periods
        ).scoreboard
        for team_index, indexed_strategy in enumerate(indexed_strategies):
            total_scores[indexed_strategy[0]] += scoreboard.score[team_index]
        indexed_strategies = list(reversed(indexed_strategies))

    winner_is_1 = total_scores[0] > total_scores[1]
    return winner_is_1
