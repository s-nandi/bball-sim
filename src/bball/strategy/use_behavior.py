from dataclasses import dataclass
from typing import Protocol
from bball.player import Player
from bball.strategy.strategy_interface import StrategyInterface


class SupportsDrive(Protocol):
    def drive(self, player: Player, time_frame: float) -> bool:
        pass


@dataclass
class UseBehavior(StrategyInterface):
    behavior: SupportsDrive

    def _after_team_set(self):
        pass

    def _drive(self):
        for player in self._team:
            self.behavior.drive(player, self._time_frame)
