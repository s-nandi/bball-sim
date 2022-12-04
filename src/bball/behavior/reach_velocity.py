from dataclasses import dataclass, field
from typing import Optional, Callable
from bball.utils import (
    Vector,
    close_to,
    ZERO_VECTOR,
    vector_angle_degrees,
    vector_length,
    angle_degrees_to_vector,
    multiply_by,
    sum_of,
    difference_between,
)
from bball.player import Player
from bball.behavior.reach_orientation import ReachOrientation


def ternary_search_for_min(
    func: Callable[[float], float],
    lower_bound: float,
    upper_bound: float,
    iterations: int = 50,
    tolerance: float = 10**-6,
) -> float:
    assert lower_bound <= upper_bound
    for _ in range(iterations):
        gap = upper_bound - lower_bound
        lower_third = lower_bound + gap / 3
        upper_third = upper_bound - gap / 3
        if func(lower_third) > func(upper_third):
            lower_bound = lower_third
        else:
            upper_bound = upper_third
    lower_eval = func(lower_bound)
    upper_eval = func(upper_bound)
    err = abs(lower_eval - upper_eval)
    assert err <= tolerance
    return lower_bound


def ideal_acceleration_multiplier(player: Player, v_target: Vector, time_frame: float):
    v_curr = player.velocity
    a_unit = angle_degrees_to_vector(
        player.orientation_degrees, player.physical_attributes.max_acceleration
    )

    def remaining_difference_after_accelerating(a_coeff):
        a_applied = multiply_by(a_unit, a_coeff * time_frame)
        v_next = sum_of(a_applied, v_curr)
        v_diff = difference_between(v_target, v_next)
        diff_magnitude = vector_length(v_diff)
        return diff_magnitude

    ideal_a_coeff = ternary_search_for_min(
        remaining_difference_after_accelerating, -1.0, 1.0
    )
    return ideal_a_coeff


@dataclass
class ReachVelocity:
    target_velocity: Vector
    time_frame: float
    target_angle_degrees: Optional[float] = field(init=False)

    def __post_init__(self):
        if close_to(self.target_velocity, ZERO_VECTOR):
            self.target_angle_degrees = None
        else:
            self.target_angle_degrees = vector_angle_degrees(self.target_velocity)

    def _fix_velocity_magnitude_assuming_alignment(self, player: Player) -> bool:
        if close_to(player.velocity, self.target_velocity):
            return False
        multiplier = ideal_acceleration_multiplier(
            player, self.target_velocity, self.time_frame
        )
        player.accelerate(multiplier)
        return True

    def drive(self, player: Player) -> bool:
        if self.target_angle_degrees is not None:
            orient = ReachOrientation(self.target_angle_degrees, self.time_frame)
            if orient.drive(player):
                return True
        if self._fix_velocity_magnitude_assuming_alignment(player):
            return True
        return False
