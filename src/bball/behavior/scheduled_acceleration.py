from typing import List, Tuple
from dataclasses import dataclass, field
from bball.player import Player
from bball.behavior.behavior_interface import BehaviorInterface
from bball.behavior.utils import acceleration_multiplier


@dataclass
class ScheduledAcceleration(BehaviorInterface):
    acceleration_with_counts: List[Tuple[float, int]]
    current_index: int = field(init=False, default=0)
    current_count: int = field(init=False, default=0)

    def _drive(self, player: Player) -> bool:
        if self.current_index >= len(self.acceleration_with_counts):
            return False
        current_acceleration_count = self.acceleration_with_counts[self.current_index]
        if self.current_count >= current_acceleration_count[1]:
            self.current_count = 0
            self.current_index += 1
            return self.drive(player, self._time_frame)
        acceleration = current_acceleration_count[0]
        player.accelerate(acceleration_multiplier(player, acceleration))
        self.current_count += 1
        return True
