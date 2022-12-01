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
from bball_server.player import Player, PlayerAttributes

Attributes = PlayerAttributes.Physical


def turn_multiplier(
    attributes: Attributes, turn_degrees: float, time_frame: float
) -> float:
    multiplier = turn_degrees / time_frame / attributes.max_turn_degrees
    return clamp(multiplier, -1.0, 1.0)


def acceleration_multiplier(
    attributes: Attributes, acceleration: float, time_frame: float
) -> float:
    multiplier = acceleration / time_frame / attributes.max_acceleration
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
        multiplier = turn_multiplier(player.physical_attributes, delta, self.time_frame)
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
        multiplier = acceleration_multiplier(
            player.physical_attributes, delta, self.time_frame
        )
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
        multiplier = acceleration_multiplier(
            player.physical_attributes, delta, self.time_frame
        )
        player.accelerate(multiplier)
        return True


@dataclass
class ReachPositionBehavior:
    target_position: Point
    time_frame: float

    def drive(self, player: Player) -> bool:
        if close_to(player.position, self.target_position):
            return StopBehavior(self.time_frame).drive(player)

        target_orientation_degrees = vector_angle_degrees(self.target_position)
        if ReachOrientationBehavior(target_orientation_degrees, self.time_frame).drive(
            player
        ):
            return True

        position_delta = difference_between(self.target_position, player.position)
        assert is_moving_in_orientation_direction(
            position_delta, player.orientation_degrees
        )

        distance = vector_length(position_delta)
        velocity_magnitude = vector_length(player.velocity)
        max_acceleration = player.physical_attributes.max_acceleration
        time = (
            float("inf")
            if approx(velocity_magnitude, 0)
            else distance / velocity_magnitude
        )
        if time > self.time_frame:
            delta = max_acceleration * self.time_frame - velocity_magnitude
        else:
            delta = time - self.time_frame
        multiplier = acceleration_multiplier(
            player.physical_attributes, delta, self.time_frame
        )
        player.accelerate(multiplier)
        return True
