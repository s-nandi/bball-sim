from dataclasses import dataclass, field
from typing import List
from bball.team import other_team_index
from bball.behavior import StandBetween
from bball.strategy.strategy_interface import StrategyInterface


@dataclass
class StandBetweenBasket(StrategyInterface):
    time_frame: float
    _behaviors: List[StandBetween] = field(init=False)

    def _after_team_set(self):
        opponent_team = self._game.teams[other_team_index(self._team_index)]
        self._behaviors = [
            StandBetween(matchup, self._game.target_hoop(matchup), self.time_frame)
            for matchup in opponent_team
        ]

    def drive(self):
        for behavior, player in zip(self._behaviors, self._team):
            behavior.drive(player)
