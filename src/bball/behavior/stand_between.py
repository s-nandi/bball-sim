from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from bball.player import Player
from bball.behavior.behavior_interface import BehaviorInterface
from bball.behavior.run_past_position import RunPastPosition
from bball.utils import midpoint_of, projected_position_of

if TYPE_CHECKING:
    from bball.utils import ObjectWithPosition


@dataclass
class StandBetween(BehaviorInterface):
    object_keep_in_front: ObjectWithPosition
    object_keep_behind: ObjectWithPosition

    def _drive(self, player: Player) -> bool:
        position_keep_behind = projected_position_of(self.object_keep_behind)
        position_keep_in_front = projected_position_of(self.object_keep_in_front)
        midpoint = midpoint_of(position_keep_behind, position_keep_in_front)
        player_size = player.physical_attributes.size
        return RunPastPosition(midpoint, 2 * player_size).drive(
            player, self._time_frame
        )
