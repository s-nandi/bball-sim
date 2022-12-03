from dataclasses import dataclass
from bball.strategy.strategy_interface import StrategyInterface


@dataclass
class CompositeStrategy(StrategyInterface):
    offensive_strategy: StrategyInterface
    defensive_strategy: StrategyInterface

    def __init__(
        self,
        offensive_strategy: StrategyInterface,
        defensive_strategy: StrategyInterface,
    ):
        self.offensive_strategy = offensive_strategy
        self.defensive_strategy = defensive_strategy

    def _after_team_set(self):
        self.offensive_strategy.for_team_index_in_game(self._team_index, self._game)
        self.defensive_strategy.for_team_index_in_game(self._team_index, self._game)

    def _drive(self):
        offensive_team_index = self._game.team_with_last_posession
        if offensive_team_index is None:
            return
        if offensive_team_index == self._team_index:
            self.offensive_strategy.drive(self._time_frame)
        else:
            self.defensive_strategy.drive(self._time_frame)