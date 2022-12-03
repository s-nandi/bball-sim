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


def distance_covered(a_max: float, v_curr: float, steps: int, time_frame: float):
    velocity_contribution = v_curr * steps * time_frame
    acceleration_contribution = steps * (steps + 1) / 2 * (a_max * time_frame**2)
    return velocity_contribution + acceleration_contribution


def triangle_distance_covered(
    a_max: float, v_curr: float, steps: int, time_frame: float
):
    slowdown_steps = v_curr / (a_max * time_frame)
    assert steps >= slowdown_steps
    rem_steps = steps - slowdown_steps
    rectangle_area = rem_steps * v_curr * time_frame
    right_triangle = slowdown_steps * v_curr * time_frame / 2
    halfway = rem_steps * time_frame / 2
    top_area = (rem_steps * time_frame) * (halfway * a_max) / 2
    return right_triangle + rectangle_area + top_area


def min_steps_needed(a_max: float, v_curr: float, distance: float, time_frame: float):
    def distance_evaluate(steps):
        return triangle_distance_covered(a_max, v_curr, steps, time_frame)

    a_lo = v_curr / (a_max * time_frame)
    a_hi = a_lo + 1
    assert a_hi > 0
    while distance_evaluate(a_hi) < distance:
        a_hi *= 2
    for _ in range(100):
        a_mid = (a_lo + a_hi) / 2
        if distance_evaluate(a_mid) < distance:
            a_lo = a_mid
        else:
            a_hi = a_mid
    return a_lo


def steady_steps_needed(
    a_max: float, v_curr: float, distance: float, time_frame: float
):
    num_steps = 0
    while distance_covered(a_max, v_curr, num_steps, time_frame) < distance:
        num_steps += 1
    return num_steps


def acceleration_for(a_max: float, v_curr: float, distance: float, time_frame: float):
    steps = 2 * steady_steps_needed(a_max, v_curr, distance / 2, time_frame)

    def evaluate(accel):
        return 2 * distance_covered(accel, v_curr, steps / 2, time_frame)

    a_lo = -a_max
    a_hi = a_max
    for _ in range(50):
        a_mid = (a_lo + a_hi) / 2
        possible_distance = evaluate(a_mid)
        if possible_distance > distance:
            a_hi = a_mid
        else:
            a_lo = a_mid
    return a_lo, steps


def highest_acceleration_without_overshoot(
    a_max: float, v_curr: float, distance: float, time_frame: float
):
    steps = min_steps_needed(a_max, v_curr, distance, time_frame)

    def evaluate(accel):
        v_next = v_curr + time_frame * accel
        curr_step = distance_covered(accel, v_curr, 1, time_frame)
        future_steps = distance_covered(-a_max, v_next, steps - 1, time_frame)
        return curr_step + future_steps

    a_lo = -a_max
    a_hi = a_max
    for _ in range(50):
        a_mid = (a_lo + a_hi) / 2
        possible_distance = evaluate(a_mid)
        if possible_distance > distance:
            a_hi = a_mid
        else:
            a_lo = a_mid
    assert evaluate(a_hi) - evaluate(a_lo) < 0.01
    return a_lo
