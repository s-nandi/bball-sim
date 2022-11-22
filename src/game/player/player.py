from typing import Iterable, List
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.types import ConvertibleToVec2d, convert_to_vec2d, Team
from game.utils import limited_velocity_func
from game.player.player_attributes import PlayerAttributes

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
    previous_accel: pymunk.Vec2d

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
        self.previous_accel = pymunk.Vec2d(0, 0)

    def __str__(self):
        return f"attr = {self.attributes}"

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield from self.shapes

    @staticmethod
    def create_body(
        attributes: PlayerAttributes, position: pymunk.Vec2d
    ) -> pymunk.Body:
        body = pymunk.Body()
        body.position = position
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
        shape.elasticity = 0.5
        shape.friction = 0.2
        return [shape]
