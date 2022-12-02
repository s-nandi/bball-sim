from dataclasses import dataclass, field
from bball.utils import (
    Vector,
    close_to,
    ZERO_VECTOR,
    vector_angle_degrees,
    vector_length,
)
from bball.player import Player
from bball.behavior.utils import (
    is_moving_in_orientation_direction,
    acceleration_multiplier,
)
from bball.behavior.reach_orientation import ReachOrientation


@dataclass
class ReachVelocity:
    target_velocity: Vector
    time_frame: float
    target_angle_degrees: float = field(init=False)

    def __post_init__(self):
        assert not close_to(self.target_velocity, ZERO_VECTOR)
        self.target_angle_degrees = vector_angle_degrees(self.target_velocity)

    def _fix_velocity_magnitude_assuming_alignment(self, player: Player) -> bool:
        if close_to(player.velocity, self.target_velocity):
            return False

        moving_in_orientation_direction = is_moving_in_orientation_direction(
            player.velocity, player.orientation_degrees
        )
        if moving_in_orientation_direction:
            delta = vector_length(self.target_velocity) - vector_length(player.velocity)
        else:
            delta = vector_length(self.target_velocity) + vector_length(player.velocity)
        multiplier = acceleration_multiplier(player, delta, self.time_frame)
        player.accelerate(multiplier)
        return True

    def drive(self, player: Player) -> bool:
        if ReachOrientation(self.target_angle_degrees, self.time_frame).drive(player):
            return True
        if self._fix_velocity_magnitude_assuming_alignment(player):
            return True
        return False
