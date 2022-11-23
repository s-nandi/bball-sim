from bball_server.physics_object import PhysicsObject
from bball_server.physics import kinematic_step


class Ball(PhysicsObject):
    def throw(self, orientation_degrees: float, strength: float) -> None:
        assert self.is_initialized
        self._orientation_degrees = orientation_degrees
        self._position, self._velocity = kinematic_step(
            self._position,
            self._velocity,
            self._orientation_degrees,
            strength,
            self._velocity_decay,
        )
