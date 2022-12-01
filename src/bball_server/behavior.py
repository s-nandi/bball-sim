from typing import List, Tuple, Optional
from dataclasses import dataclass, field
from bball_server.utils import (
    Point,
    Vector,
    close_to,
    ZERO_VECTOR,
    clamp,
    turn_degrees_required,
    vector_angle_degrees,
    vector_length,
    approx,
    difference_between,
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


@dataclass
class ReachVelocityBehavior:
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
        if ReachOrientationBehavior(self.target_angle_degrees, self.time_frame).drive(
            player
        ):
            return True
        if self._fix_velocity_magnitude_assuming_alignment(player):
            return True
        return False


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


@dataclass
class ScheduledAccelerationBehavior:
    acceleration_with_counts: List[Tuple[float, int]]
    current_index: int = field(init=False, default=0)
    current_count: int = field(init=False, default=0)

    def drive(self, player: Player) -> bool:
        if self.current_index >= len(self.acceleration_with_counts):
            return False
        current_acceleration_count = self.acceleration_with_counts[self.current_index]
        if self.current_count >= current_acceleration_count[1]:
            self.current_count = 0
            self.current_index += 1
            return self.drive(player)
        acceleration = current_acceleration_count[0]
        player.accelerate(acceleration_multiplier(player, acceleration))
        self.current_count += 1
        return True


def distance_covered(steps: int, a_max, time_frame):
    return steps * (steps + 1) * a_max * time_frame**2


def min_steps_needed(a_max, distance, time_frame):
    num_steps = 0
    while distance_covered(num_steps, a_max, time_frame) < distance:
        num_steps += 1
    return num_steps


def acceleration_for(distance: float, steps: int, a_max, time_frame):
    a_lo = 0
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


@dataclass
class ReachPositionBehavior:
    target_position: Point
    time_frame: float
    _scheduled_behavior: Optional[ScheduledAccelerationBehavior] = field(
        init=False, default=None
    )

    def drive(self, player: Player) -> bool:
        if close_to(player.position, self.target_position):
            return StopBehavior(self.time_frame).drive(player)

        if self._scheduled_behavior is None and StopBehavior(self.time_frame).drive(
            player
        ):
            return True
        position_delta = difference_between(self.target_position, player.position)
        target_orientation_degrees = vector_angle_degrees(position_delta)
        if ReachOrientationBehavior(target_orientation_degrees, self.time_frame).drive(
            player
        ):
            self._scheduled_behavior = None
            return True

        if self._scheduled_behavior is None:
            distance = vector_length(position_delta)
            max_acceleration = player.physical_attributes.max_acceleration

            num_steps = min_steps_needed(max_acceleration, distance, self.time_frame)
            target_acceleration = acceleration_for(
                distance, num_steps, max_acceleration, self.time_frame
            )
            self._scheduled_behavior = ScheduledAccelerationBehavior(
                [
                    (target_acceleration, num_steps),
                    (0, 1),
                    (-target_acceleration, num_steps),
                ]
            )
        return self._scheduled_behavior.drive(player)
