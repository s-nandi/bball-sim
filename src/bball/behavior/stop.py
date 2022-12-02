from dataclasses import dataclass
from bball.utils import close_to, vector_length
from bball.player import Player
from bball.behavior.utils import (
    is_moving_in_orientation_direction,
    acceleration_multiplier,
)


@dataclass
class Stop:
    time_frame: float

    def drive(self, player: Player) -> bool:
        if close_to(player.velocity, (0, 0)):
            return False
        moving_in_orientation_direction = is_moving_in_orientation_direction(
            player.velocity, player.orientation_degrees
        )
        if moving_in_orientation_direction:
            delta = -vector_length(player.velocity)
        else:
            delta = vector_length(player.velocity)
        multiplier = acceleration_multiplier(player, delta, self.time_frame)
        player.accelerate(multiplier)
        return True
