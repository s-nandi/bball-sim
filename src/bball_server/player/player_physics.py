from bball_server.player.player_move import PlayerMove
from bball_server.physics_object import PhysicsObject
from bball_server.player.player_attributes import PlayerAttributes
from bball_server.utils import to_radians


class PlayerPhysics(PhysicsObject):
    def __init__(self, attributes: PlayerAttributes):
        super().__init__(attributes.mass, attributes.velocity_decay)

    def step(self, action: PlayerMove, time_step: float) -> None:
        assert self.is_initialized
        super().turn(to_radians(action.turn_degrees), time_step)
        super().accelerate(action.acceleration, self._body.angle, time_step)
