from typing import Optional
from dataclasses import dataclass, field
from bball.utils import (
    Point,
    close_to,
    vector_angle_degrees,
    vector_length,
    approx,
    difference_between,
)
from bball.player import Player
from bball.behavior.reach_orientation import ReachOrientation
from bball.behavior.stop import Stop
from bball.behavior.scheduled_acceleration import ScheduledAcceleration


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
class ReachPosition:
    target_position: Point
    time_frame: float
    _scheduled_behavior: Optional[ScheduledAcceleration] = field(
        init=False, default=None
    )

    def drive(self, player: Player) -> bool:
        if close_to(player.position, self.target_position):
            return Stop(self.time_frame).drive(player)

        if self._scheduled_behavior is None and Stop(self.time_frame).drive(player):
            return True
        position_delta = difference_between(self.target_position, player.position)
        target_orientation_degrees = vector_angle_degrees(position_delta)
        if ReachOrientation(target_orientation_degrees, self.time_frame).drive(player):
            self._scheduled_behavior = None
            return True

        if self._scheduled_behavior is None:
            distance = vector_length(position_delta)
            max_acceleration = player.physical_attributes.max_acceleration

            num_steps = min_steps_needed(max_acceleration, distance, self.time_frame)
            target_acceleration = acceleration_for(
                distance, num_steps, max_acceleration, self.time_frame
            )
            self._scheduled_behavior = ScheduledAcceleration(
                [
                    (target_acceleration, num_steps),
                    (0, 1),
                    (-target_acceleration, num_steps),
                ]
            )
        return self._scheduled_behavior.drive(player)
