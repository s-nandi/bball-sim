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
from bball.behavior.reach_orientation import ReachOrientation
from bball.behavior.stop import Stop
from bball.behavior.scheduled_acceleration import ScheduledAcceleration
from bball.behavior.utils import acceleration_for, min_steps_needed


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
                max_acceleration, distance, self.time_frame
            )
            self._scheduled_behavior = ScheduledAcceleration(
                [
                    (target_acceleration, num_steps),
                    (0, 1),
                    (-target_acceleration, num_steps),
                ]
            )
        return self._scheduled_behavior.drive(player)
