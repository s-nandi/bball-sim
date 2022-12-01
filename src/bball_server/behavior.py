from dataclasses import dataclass, field
from bball_server.utils import (
    Vector,
    close_to,
    ZERO_VECTOR,
    clamp,
    turn_degrees_required,
    vector_angle_degrees,
    vector_length,
    approx,
)
from bball_server.player import Player, PlayerAttributes

Attributes = PlayerAttributes.Physical


def turn_multiplier(attributes: Attributes, turn_degrees: float) -> float:
    multiplier = turn_degrees / attributes.max_turn_degrees
    return clamp(multiplier, -1.0, 1.0)


def acceleration_multiplier(attributes: Attributes, acceleration: float) -> float:
    multiplier = acceleration / attributes.max_acceleration
    return clamp(multiplier, -1.0, 1.0)


def should_accelerate_forward_assuming_alignment(
    current_velocity: Vector, current_orientation_degrees: float
) -> bool:
    accelerate_forward = True
    if not close_to(current_velocity, (0, 0)):
        angle_difference = turn_degrees_required(
            vector_angle_degrees(current_velocity), current_orientation_degrees
        )
        accelerate_forward = approx(angle_difference, 0)
        accelerate_backward = approx(angle_difference, -180) or approx(
            angle_difference, 180
        )
        assert accelerate_forward ^ accelerate_backward, f"{angle_difference}"
    return accelerate_forward


@dataclass
class ReachVelocityBehavior:
    target_velocity: Vector
    target_angle_degrees: float = field(init=False)

    def __post_init__(self):
        assert not close_to(self.target_velocity, ZERO_VECTOR)
        self.target_angle_degrees = vector_angle_degrees(self.target_velocity)

    def _correct_orientation(self, player: Player) -> bool:
        return approx(
            turn_degrees_required(
                player.orientation_degrees, self.target_angle_degrees
            ),
            0,
        )

    def _fix_orientation(self, player: Player) -> bool:
        if self._correct_orientation(player):
            return False
        delta = turn_degrees_required(
            player.orientation_degrees, self.target_angle_degrees
        )
        multiplier = turn_multiplier(player.physical_attributes, delta)
        player.turn(multiplier)
        return True

    def _fix_velocity_magnitude(self, player: Player) -> bool:
        if close_to(player.velocity, self.target_velocity):
            return False

        accelerate_forward = should_accelerate_forward_assuming_alignment(
            player.velocity, player.orientation_degrees
        )
        if accelerate_forward:
            delta = vector_length(self.target_velocity) - vector_length(player.velocity)
        else:
            delta = vector_length(self.target_velocity) + vector_length(player.velocity)
        multiplier = acceleration_multiplier(player.physical_attributes, delta)
        player.accelerate(multiplier)
        return True

    def drive(self, player: Player) -> bool:
        if self._fix_orientation(player):
            return True
        if self._fix_velocity_magnitude(player):
            return True
        return False


class StopBehavior:
    def drive(self, player: Player) -> bool:
        if close_to(player.velocity, (0, 0)):
            return False
        accelerate_forward = should_accelerate_forward_assuming_alignment(
            player.velocity, player.orientation_degrees
        )
        if accelerate_forward:
            delta = -vector_length(player.velocity)
        else:
            delta = vector_length(player.velocity)
        multiplier = acceleration_multiplier(player.physical_attributes, delta)
        player.accelerate(multiplier)
        return True
