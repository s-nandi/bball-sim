from bball.player import Player
from bball.behavior.behavior_interface import BehaviorInterface
from bball.behavior.reach_velocity import ReachVelocity


class Stop(BehaviorInterface):
    def _drive(self, player: Player) -> bool:
        return ReachVelocity((0, 0)).drive(player, self._time_frame)
