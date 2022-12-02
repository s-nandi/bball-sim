from dataclasses import dataclass
from typing import Union
from bball.court import Hoop
from bball.player import Player
from bball.behavior.run_past_position import RunPastPosition
from bball.behavior.stop import Stop
from bball.utils import midpoint_of, sum_of, in_between_of, Point

ObjectWithPosition = Union[Player, Hoop, Point]


def position_of(obj: ObjectWithPosition) -> Point:
    if isinstance(obj, tuple):
        return obj
    return obj.position


def projected_position_of(obj: ObjectWithPosition) -> Point:
    if isinstance(obj, Player):
        return sum_of(obj.position, obj.velocity)
    return position_of(obj)


@dataclass
class StandBetween:
    object_keep_in_front: ObjectWithPosition
    object_keep_behind: ObjectWithPosition
    time_frame: float

    def drive(self, player: Player) -> bool:
        position_keep_behind = projected_position_of(self.object_keep_behind)
        position_keep_in_front = projected_position_of(self.object_keep_in_front)
        midpoint = midpoint_of(position_keep_behind, position_keep_in_front)
        midpoint_is_in_front = in_between_of(
            player.position, position_keep_behind, midpoint
        )
        if midpoint_is_in_front:
            return Stop(self.time_frame).drive(player)
        return RunPastPosition(midpoint, self.time_frame).drive(player)
