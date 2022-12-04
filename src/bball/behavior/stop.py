from dataclasses import dataclass
from bball.player import Player
from bball.behavior.reach_velocity import ReachVelocity


@dataclass
class Stop:
    time_frame: float

    def drive(self, player: Player) -> bool:
        return ReachVelocity((0, 0), self.time_frame).drive(player)
