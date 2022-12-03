from dataclasses import dataclass, field
from typing import Optional, List
from bball.behavior import ReachPosition
from bball.utils import distance_between
from bball.strategy.strategy_interface import StrategyInterface


@dataclass
class RunToBasketAndShoot(StrategyInterface):
    time_frame: float
    distance_threshold: float
    _behaviors: List[Optional[ReachPosition]] = field(init=False)

    def _after_team_set(self):
        self._behaviors = [
            ReachPosition(self._game.target_hoop(player).position, self.time_frame)
            for player in self._team
        ]

    def drive(self):
        for behavior, player in zip(self._behaviors, self._team):
            target_hoop = self._game.target_hoop(player)
            close_enough = (
                distance_between(player.position, target_hoop.position)
                <= self.distance_threshold
            )
            if player.has_ball and close_enough:
                player.shoot_at(target_hoop.position, 1)
            else:
                assert behavior is not None
                behavior.drive(player)
