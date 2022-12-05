from dataclasses import dataclass
from typing import Tuple
from bball.validator import valid_shot_value

Score = Tuple[float, float]
Possessions = Tuple[int, int]


def error_message(team_index: int) -> str:
    return f"Invalid team index {team_index}, must be 0 or 1"


@dataclass
class Scoreboard:
    _score_1: float = 0
    _score_2: float = 0
    _posessions_1: int = 0
    _posessions_2: int = 0

    @property
    def score(self) -> Score:
        return (self._score_1, self._score_2)

    @property
    def possessions(self) -> Possessions:
        return (self._posessions_1, self._posessions_2)

    def increment_score(self, team_index: int, value: float):
        assert valid_shot_value(value)
        if team_index == 0:
            self._score_1 += value
        elif team_index == 1:
            self._score_2 += value
        else:
            assert False, error_message(team_index)

    def increment_possessions(self, team_index: int):
        if team_index == 0:
            self._posessions_1 += 1
        elif team_index == 1:
            self._posessions_2 += 1
        else:
            assert False, error_message(team_index)
