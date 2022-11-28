from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from dataclasses import dataclass
from bball_server.court.three_point_line import ThreePointLine

if TYPE_CHECKING:
    from bball_server.player import Player


@dataclass
class Hoop:
    x_position: float
    y_position: float
    three_point_line: ThreePointLine

    def other_hoop(self, width: float) -> Hoop:
        return Hoop(
            width - self.x_position,
            self.y_position,
            self.three_point_line.other_line(width),
        )

    @property
    def position(self) -> Tuple[float, float]:
        return (self.x_position, self.y_position)

    def is_beyond_three_point_line(self, player: Player) -> bool:
        return self.three_point_line.is_beyond(player.position)
