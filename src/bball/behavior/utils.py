from bball.utils import (
    Vector,
    close_to,
    clamp,
    turn_degrees_required,
    vector_angle_degrees,
    approx,
)
from bball.player import Player


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


def distance_covered(steps: int, a_max: float, time_frame: float):
    return steps * (steps + 1) * a_max * time_frame**2


def min_steps_needed(a_max: float, distance: float, time_frame: float):
    num_steps = 0
    while distance_covered(num_steps, a_max, time_frame) < distance:
        num_steps += 1
    return num_steps


def acceleration_for(a_max: float, distance: float, time_frame: float):
    steps = min_steps_needed(a_max, distance, time_frame)
    a_lo = 0.0
    a_hi = a_max
    while True:
        a_mid = (a_lo + a_hi) / 2
        possible_distance = distance_covered(steps, a_mid, time_frame)
        if approx(possible_distance, distance):
            return a_mid
        if possible_distance > distance:
            a_hi = a_mid
        else:
            a_lo = a_mid
