from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from bball.game import Game
    from bball.team import Team


class StrategyInterface(ABC):
    _game: Game
    _team_index: int

    @property
    def _team(self) -> Team:
        return self._game.teams[self._team_index]

    def for_team_index_in_game(self, team_index: int, game: Game) -> StrategyInterface:
        self._game = game
        self._team_index = team_index
        self._after_team_set()
        return self

    @abstractmethod
    def _after_team_set(self) -> None:
        pass

    @abstractmethod
    def drive(self):
        pass
