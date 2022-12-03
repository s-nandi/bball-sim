from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from bball.player import Player
from bball.behavior.run_past_position import RunPastPosition
from bball.behavior.stop import Stop
from bball.utils import midpoint_of, in_between_of, projected_position_of

if TYPE_CHECKING:
    from bball.utils import ObjectWithPosition


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
        player_size = player.physical_attributes.size
        return RunPastPosition(midpoint, 2 * player_size, self.time_frame).drive(player)
