from dataclasses import dataclass
from bball.utils import Point, close_to, vector_angle_degrees, difference_between
from bball.player import Player
from bball.behavior.reach_orientation import ReachOrientationBehavior
from bball.behavior.stop import StopBehavior
from bball.behavior.utils import is_moving_in_orientation_direction


@dataclass
class RunPastPositionBehavior:
    target_position: Point
    time_frame: float

    def drive(self, player: Player) -> bool:
        if close_to(player.position, self.target_position):
            return StopBehavior(self.time_frame).drive(player)

        position_delta = difference_between(self.target_position, player.position)
        target_orientation_degrees = vector_angle_degrees(position_delta)
        if ReachOrientationBehavior(target_orientation_degrees, self.time_frame).drive(
            player
        ):
            return True
        ran_past = not is_moving_in_orientation_direction(
            position_delta, player.orientation_degrees
        )
        if ran_past:
            return StopBehavior(self.time_frame).drive(player)
        player.accelerate(1)
        return True
