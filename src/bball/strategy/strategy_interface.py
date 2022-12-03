from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from bball.utils import approx

if TYPE_CHECKING:
    from bball.game import Game
    from bball.team import Team


class StrategyInterface(ABC):
    _game: Game
    _team_index: int
    _time_frame: float
    _has_run: bool = False

    @property
    def _team(self) -> Team:
        return self._game.teams[self._team_index]

    def for_team_index_in_game(self, team_index: int, game: Game) -> StrategyInterface:
        self._game = game
        self._team_index = team_index
        self.after_team_set()
        return self

    def drive(self, time_frame: float):
        if not self._has_run:
            self._has_run = True
            self._time_frame = time_frame
            self._after_team_set()
        assert approx(self._time_frame, time_frame)
        self._drive()

    def after_team_set(self):
        if not self._has_run:
            return
        self._after_team_set()

    @abstractmethod
    def _after_team_set(self) -> None:
        pass

    @abstractmethod
    def _drive(self):
        pass
