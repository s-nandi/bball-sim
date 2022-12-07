from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from bball.court.three_point_line import ThreePointLine
from bball.utils import distance_between

if TYPE_CHECKING:
    from bball.utils import Point
    from bball.player import Player


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
    def position(self) -> Point:
        return (self.x_position, self.y_position)

    def is_beyond_three_point_line(self, position: Point) -> bool:
        return self.three_point_line.is_beyond(position)

    def value_of_shot_from(self, position: Point) -> int:
        return 3 if self.is_beyond_three_point_line(position) else 2

    def expected_value_of_shot_by(self, player: Player) -> float:
        distance = distance_between(player.position, self.position)
        probability_function = player.skill_attributes.shot_probability
        probability = probability_function(distance)
        value = self.value_of_shot_from(player.position)
        return value * probability
