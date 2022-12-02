from dataclasses import dataclass, field
from typing import Optional, List
from bball.game import Game
from bball.team import Team
from bball.behavior import ReachPosition
from bball.utils import distance_between
from bball.strategy.strategy_interface import StrategyInterface


@dataclass
class RunToBasket(StrategyInterface):
    team: Team
    time_frame: float
    distance_threshold: float
    _behaviors: List[Optional[ReachPosition]] = field(init=False)

    def __post_init__(self):
        self._behaviors = [None for _ in self.team]

    def drive(self, game: Game):
        for player_index, player in enumerate(self.team):
            target_hoop = game.target_hoop(player)
            if self._behaviors[player_index] is None:
                self._behaviors[player_index] = ReachPosition(
                    target_hoop.position, self.time_frame
                )

        for behavior, player in zip(self._behaviors, self.team):
            close_enough = (
                distance_between(player.position, target_hoop.position)
                <= self.distance_threshold
            )
            if player.has_ball and close_enough:
                player.shoot_at(target_hoop.position, 1)
            else:
                assert behavior is not None
                behavior.drive(player)
