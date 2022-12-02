from dataclasses import dataclass
from bball_server.utils import close_to, vector_length
from bball_server.player import Player
from bball_server.behavior.utils import (
    is_moving_in_orientation_direction,
    acceleration_multiplier,
)


@dataclass
class StopBehavior:
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
