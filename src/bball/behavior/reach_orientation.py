from dataclasses import dataclass
from bball.utils import turn_degrees_required, approx
from bball.player import Player
from bball.behavior.behavior_interface import BehaviorInterface
from bball.behavior.utils import turn_multiplier


@dataclass
class ReachOrientation(BehaviorInterface):
    target_angle_degrees: float

    def _correct_orientation(self, player: Player) -> bool:
        return approx(
            turn_degrees_required(
                player.orientation_degrees, self.target_angle_degrees
            ),
            0,
        )

    def _drive(self, player: Player) -> bool:
        if self._correct_orientation(player):
            return False
        delta = turn_degrees_required(
            player.orientation_degrees, self.target_angle_degrees
        )
        multiplier = turn_multiplier(player, delta / self._time_frame)
        player.turn(multiplier)
        return True
