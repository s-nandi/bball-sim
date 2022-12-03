from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from bball.behavior import ReachPosition
from bball.utils import distance_between, position_of
from bball.strategy.strategy_interface import StrategyInterface

if TYPE_CHECKING:
    from bball.utils import ObjectWithPosition


@dataclass
class RunToTargetAndShoot(StrategyInterface):
    target: ObjectWithPosition
    distance_threshold: float
    _behaviors: List[Optional[ReachPosition]] = field(init=False)

    def _after_team_set(self):
        self._behaviors = [
            ReachPosition(position_of(self.target), self._time_frame)
            for _ in self._team
        ]

    def _drive(self):
        for behavior, player in zip(self._behaviors, self._team):
            close_enough = (
                distance_between(player.position, position_of(self.target))
                <= self.distance_threshold
            )
            if player.has_ball and close_enough:
                target_hoop = self._game.target_hoop(player)
                player.shoot_at(target_hoop.position, 10)
            else:
                behavior.drive(player)
