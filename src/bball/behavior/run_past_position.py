from dataclasses import dataclass
from bball.utils import (
    Point,
    close_to,
    vector_angle_degrees,
    difference_between,
    distance_between,
    sum_of,
    angle_degrees_to_vector,
    in_between_of,
    vector_length,
)
from bball.player import Player
from bball.behavior.behavior_interface import BehaviorInterface
from bball.behavior.reach_orientation import ReachOrientation
from bball.behavior.stop import Stop
from bball.behavior.utils import (
    highest_acceleration_without_overshoot,
    acceleration_multiplier,
)


@dataclass
class RunPastPosition(BehaviorInterface):
    target_position: Point
    distance_threshold: float

    def _drive(self, player: Player) -> bool:
        if close_to(player.position, self.target_position, self.distance_threshold):
            return Stop().drive(player, self._time_frame)

        position_delta = difference_between(self.target_position, player.position)

        target_orientation_degrees = vector_angle_degrees(position_delta)
        ReachOrientation(target_orientation_degrees).drive(player, self._time_frame)

        distance = distance_between(self.target_position, player.position)
        extrapolated_position = sum_of(
            player.position,
            angle_degrees_to_vector(player.orientation_degrees, distance + 10),
        )
        good_direction = in_between_of(
            self.target_position, player.position, extrapolated_position
        )
        ran_past = not good_direction
        if ran_past:
            return Stop().drive(player, self._time_frame)
        a_max = player.physical_attributes.max_acceleration
        v_curr = vector_length(player.velocity)

        desired_acceleration = highest_acceleration_without_overshoot(
            a_max, v_curr, distance, self._time_frame
        )
        multiplier = acceleration_multiplier(player, desired_acceleration)
        player.accelerate(multiplier)
        return True
