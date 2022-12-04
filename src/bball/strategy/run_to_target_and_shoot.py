from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
from bball.behavior import RunPastPosition
from bball.utils import distance_between, position_of, DEFAULT_EPS
from bball.strategy.strategy_interface import StrategyInterface

if TYPE_CHECKING:
    from bball.utils import ObjectWithPosition


@dataclass
class RunToTargetAndShoot(StrategyInterface):
    target: ObjectWithPosition
    distance_threshold: float
    _behaviors: List[RunPastPosition] = field(init=False)

    def update_behaviors(self):
        self._behaviors = [
            RunPastPosition(position_of(self.target), DEFAULT_EPS, self._time_frame)
            for _ in self._team
        ]

    def _after_team_set(self):
        self.update_behaviors()

    def _drive(self):
        self.update_behaviors()
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
