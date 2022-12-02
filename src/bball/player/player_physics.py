from bball.player.player_move import PlayerMove
from bball.physics_object import PhysicsObject
from bball.player.player_attributes import PlayerAttributes
from bball.utils import to_radians


class PlayerPhysics(PhysicsObject):
    def __init__(self, physical_attributes: PlayerAttributes.Physical):
        super().__init__(physical_attributes.mass, physical_attributes.velocity_decay)

    def _step(self, move: PlayerMove, time_step: float) -> bool:
        assert self.is_initialized
        super().turn(to_radians(move.turn_degrees), time_step)
        super().accelerate(move.acceleration, time_step)
        return False
