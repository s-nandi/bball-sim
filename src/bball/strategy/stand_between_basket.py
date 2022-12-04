from typing import List
from bball.team import other_team_index
from bball.behavior import StandBetween
from bball.strategy.strategy_interface import StrategyInterface


class StandBetweenBasket(StrategyInterface):
    _behaviors: List[StandBetween]

    def _after_team_set(self):
        opponent_team = self._game.teams[other_team_index(self._team_index)]
        self._behaviors = [
            StandBetween(matchup, self._game.target_hoop(matchup))
            for matchup in opponent_team
        ]

    def _drive(self):
        for behavior, player in zip(self._behaviors, self._team):
            behavior.drive(player, self._time_frame)
