from typing import Optional
from dataclasses import dataclass, field
from bball.utils import (
    Point,
    close_to,
    vector_angle_degrees,
    vector_length,
    difference_between,
)
from bball.player import Player
from bball.behavior.behavior_interface import BehaviorInterface
from bball.behavior.reach_orientation import ReachOrientation
from bball.behavior.stop import Stop
from bball.behavior.scheduled_acceleration import ScheduledAcceleration
from bball.behavior.utils import acceleration_for


@dataclass
class ReachPosition(BehaviorInterface):
    target_position: Point
    _scheduled_behavior: Optional[ScheduledAcceleration] = field(
        init=False, default=None
    )

    def _drive(self, player: Player) -> bool:
        if close_to(player.position, self.target_position):
            return Stop().drive(player, self._time_frame)

        if self._scheduled_behavior is None and Stop().drive(player, self._time_frame):
            return True
        position_delta = difference_between(self.target_position, player.position)
        target_orientation_degrees = vector_angle_degrees(position_delta)
        if ReachOrientation(target_orientation_degrees).drive(player, self._time_frame):
            self._scheduled_behavior = None
            return True

        if self._scheduled_behavior is None:
            distance = vector_length(position_delta)
            max_acceleration = player.physical_attributes.max_acceleration
            target_acceleration, num_steps = acceleration_for(
                max_acceleration, 0.0, distance, self._time_frame
            )
            self._scheduled_behavior = ScheduledAcceleration(
                [
                    (target_acceleration, num_steps / 2),
                    (0, 1),
                    (-target_acceleration, num_steps / 2),
                ]
            )
        return self._scheduled_behavior.drive(player, self._time_frame)
