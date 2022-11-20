from typing import Iterable
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.types import ConvertibleToVec2d
from game.utils import limited_velocity_func
from game.scene.player_attributes import PlayerAttributes


def appliable_force(
    direction: pymunk.Vec2d, acceleration: float, attributes: PlayerAttributes
) -> pymunk.Vec2d:
    force_magnitude = attributes.mass * min(attributes.max_acceleration, acceleration)
    return direction.scale_to_length(force_magnitude)


class Player(PhysicsObject):
    body: pymunk.Body
    shape: pymunk.Shape

    def __init__(
        self,
        attributes: PlayerAttributes,
        position: pymunk.Vec2d,
    ):
        self.attributes = attributes
        self.body = self.create_body(
            attributes.mass, attributes.size, attributes.max_speed, position
        )
        self.shape = self.create_shape(attributes.size, self.body)

    def __str__(self):
        return (
            f"accel = {self.acceleration} speed = {self.speed} attr = {self.attributes}"
        )

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield self.shape

    @staticmethod
    def create_body(
        mass: float, size: float, max_speed: float, position: pymunk.Vec2d
    ) -> pymunk.Body:
        moment = pymunk.moment_for_circle(mass, 0, size)
        body = pymunk.Body(mass, moment, pymunk.Body.DYNAMIC)
        body.position = position
        body.velocity_func = limited_velocity_func(max_speed)
        return body

    @staticmethod
    def create_shape(size: float, body: pymunk.Body) -> pymunk.Shape:
        shape = pymunk.Circle(body, size)
        # TODO: Should player vs player collisions have friction?
        return shape

    @property
    def speed(self) -> float:
        return self.body.velocity.length

    @property
    def acceleration(self) -> float:
        return self.body.force.length / self.body.mass

    def move(self, direction: ConvertibleToVec2d, acceleration: float) -> None:
        direction = pymunk.Vec2d(*direction)
        force = appliable_force(direction, acceleration, self.attributes)
        self.body.apply_force_at_local_point(force)

        assert self.acceleration <= self.attributes.max_acceleration
        assert self.speed <= self.attributes.max_speed
