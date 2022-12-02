from dataclasses import dataclass
from bball.utils import turn_degrees_required, approx
from bball.player import Player
from bball.behavior.utils import turn_multiplier


@dataclass
class ReachOrientationBehavior:
    target_angle_degrees: float
    time_frame: float

    def _correct_orientation(self, player: Player) -> bool:
        return approx(
            turn_degrees_required(
                player.orientation_degrees, self.target_angle_degrees
            ),
            0,
        )

    def drive(self, player: Player) -> bool:
        if self._correct_orientation(player):
            return False
        delta = turn_degrees_required(
            player.orientation_degrees, self.target_angle_degrees
        )
        multiplier = turn_multiplier(player, delta, self.time_frame)
        player.turn(multiplier)
        return True
