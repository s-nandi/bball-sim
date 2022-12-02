from dataclasses import dataclass
from typing import Tuple
from bball.validator import valid_shot_value

Score = Tuple[float, float]


@dataclass
class Scoreboard:
    _score_1: float = 0
    _score_2: float = 0

    @property
    def score(self) -> Score:
        return (self._score_1, self._score_2)

    def increment(self, team_index: int, value: float):
        assert valid_shot_value(value)
        if team_index == 0:
            self._score_1 += value
        elif team_index == 1:
            self._score_2 += value
        else:
            assert False, f"Invalid team index {team_index}, must be 0 or 1"
