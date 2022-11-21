from typing import Iterable, List
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.types import ConvertibleToVec2d, convert_to_vec2d, Team
from game.utils import limited_velocity_func
from game.player.player_attributes import PlayerAttributes


def appliable_force(
    direction: pymunk.Vec2d, acceleration: float, attributes: PlayerAttributes
) -> pymunk.Vec2d:
    force_magnitude = attributes.mass * min(attributes.max_acceleration, acceleration)
    return direction.scale_to_length(force_magnitude)


PLAYER_DIMENSIONS_RATIO = 0.4


def width_for_size(size: float) -> float:
    return size * PLAYER_DIMENSIONS_RATIO


def height_for_size(size: float) -> float:
    return size


class Player(PhysicsObject):
    attributes: PlayerAttributes
    body: pymunk.Body
    shapes: List[pymunk.Shape]
    team: Team

    def __init__(
        self,
        attributes: PlayerAttributes,
        position: ConvertibleToVec2d,
        team: Team,
    ):
        position = convert_to_vec2d(position)
        self.attributes = attributes
        self.body = self.create_body(attributes, position)
        self.shapes = self.create_shapes(attributes, self.body)
        self.team = team

    def __str__(self):
        return (
            f"accel = {self.acceleration} speed = {self.speed} attr = {self.attributes}"
        )

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield from self.shapes

    @staticmethod
    def create_body(
        attributes: PlayerAttributes, position: pymunk.Vec2d
    ) -> pymunk.Body:
        # moment = pymunk.moment_for_box(
        #     attributes.mass,
        #     (width_for_size(attributes.size), height_for_size(attributes.size)),
        # )
        # body = pymunk.Body(attributes.mass, moment, )
        body = pymunk.Body(0, 0, body_type=pymunk.Body.DYNAMIC)
        body.position = position
        body.velocity = pymunk.Vec2d(0, 0)
        body.force = pymunk.Vec2d(0, 0)
        body.velocity_func = limited_velocity_func(attributes.max_speed)
        return body

    @staticmethod
    def create_shapes(
        attributes: PlayerAttributes, body: pymunk.Body
    ) -> List[pymunk.Shape]:
        shape = pymunk.Poly.create_box(
            body,
            (width_for_size(attributes.size), height_for_size(attributes.size)),
            0.2,
        )
        shape.mass = attributes.mass
        shape.elasticity = 0.01
        shape.friction = 0
        # shape = pymunk.Circle(body, attributes.size / 2, (0, attributes.size))
        # shape.mass = attributes.mass / 2
        # shape2 = pymunk.Circle(body, attributes.size / 2, (0, -attributes.size))
        # shape2.mass = attributes.mass / 2
        # # TODO: Should player vs player collisions have friction?
        return [shape]

    @property
    def speed(self) -> float:
        return self.body.velocity.length

    @property
    def acceleration(self) -> float:
        return self.body.force / self.body.mass

    def apply_friction(self, friction_coeff: float) -> None:
        current_force = self.body.force
        friction_force = -current_force * friction_coeff
        self.body.apply_force_at_local_point(friction_force)
