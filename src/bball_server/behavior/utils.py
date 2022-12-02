from bball_server.utils import (
    Vector,
    close_to,
    clamp,
    turn_degrees_required,
    vector_angle_degrees,
    approx,
)
from bball_server.player import Player


def turn_multiplier(player: Player, turn_degrees: float, time_frame: float) -> float:
    multiplier = turn_degrees / time_frame / player.physical_attributes.max_turn_degrees
    return clamp(multiplier, -1.0, 1.0)


def acceleration_multiplier(
    player: Player, acceleration: float, time_frame: float = 1.0
) -> float:
    multiplier = acceleration / time_frame / player.physical_attributes.max_acceleration
    return clamp(multiplier, -1.0, 1.0)


def is_moving_in_orientation_direction(
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
