from bball_server.physics import add_angle, kinematic_step
from bball_server.player.player_move import PlayerMove
from bball_server.physics_object import PhysicsObject
from bball_server.player.player_attributes import PlayerAttributes


class PlayerPhysics(PhysicsObject):
    def __init__(self, attributes: PlayerAttributes):
        super().__init__(attributes.mass, attributes.velocity_decay)

    def step(self, action: PlayerMove) -> None:
        assert self.is_initialized
        self._orientation_degrees = add_angle(
            self._orientation_degrees, action.turn_degrees
        )
        self._velocity = self._velocity.rotated_degrees(action.turn_degrees)
        self._position, self._velocity = kinematic_step(
            self._position,
            self._velocity,
            self._orientation_degrees,
            action.acceleration,
            self._velocity_decay,
        )
