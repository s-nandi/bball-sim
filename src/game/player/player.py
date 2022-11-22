from typing import Iterable, Tuple
import pymunk
import pygame
from physics_lib import PhysicsObject, PhysicsComponent
from game.types import ConvertibleToVec2d, convert_to_vec2d, Team
from game.utils import limited_velocity_func
from game.player.player_attributes import PlayerAttributes
from game.draw import draw_polygon, Color

PLAYER_DIMENSIONS_RATIO = 0.4


def width_for_size(size: float) -> float:
    return size * PLAYER_DIMENSIONS_RATIO


def height_for_size(size: float) -> float:
    return size


COLOR_TEAM_0 = Color(226, 218, 219, 255)
COLOR_TEAM_1 = Color(218, 226, 223, 255)
COLOR_WITH_BALL = Color(238, 103, 48, 255)
COLOR_WITHOUT_BALL = Color(255, 255, 255, 255)


class Player(PhysicsObject):
    attributes: PlayerAttributes
    body: pymunk.Body
    shape: pymunk.Shape
    team: Team
    has_ball: bool = False

    def __init__(
        self,
        attributes: PlayerAttributes,
        position: ConvertibleToVec2d,
        team: Team,
    ):
        position = convert_to_vec2d(position)
        self.attributes = attributes
        self.body = self.create_body(attributes, position)
        self.shape = self.create_shapes(attributes, self.body)
        self.team = team

    def __str__(self):
        return f"attr = {self.attributes}"

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield self.shape

    @staticmethod
    def create_body(
        attributes: PlayerAttributes, position: pymunk.Vec2d
    ) -> pymunk.Body:
        body = pymunk.Body()
        body.position = position
        body.velocity_func = limited_velocity_func(attributes.max_speed)
        return body

    @staticmethod
    def create_shapes(attributes: PlayerAttributes, body: pymunk.Body) -> pymunk.Shape:
        shape = pymunk.Poly.create_box(
            body,
            (width_for_size(attributes.size), height_for_size(attributes.size)),
            0.2,
        )
        shape.mass = attributes.mass
        shape.elasticity = 0.5
        shape.friction = 0.2
        return shape

    def draw(self, screen: pygame.Surface, scale: float) -> None:
        outline_color, fill_color = self.player_color()
        size = self.attributes.size
        smaller_dimension = min(width_for_size(size), height_for_size(size))

        radius = smaller_dimension / 3.5
        vertices = self.shape.get_vertices()
        vertices = list(map(lambda v: v + self.body.position, vertices))
        draw_polygon(
            screen,
            vertices,
            radius=radius,
            outline_color=outline_color,
            fill_color=fill_color,
            scale=scale,
        )

    def player_color(self) -> Tuple[Color, Color]:
        base_color = COLOR_TEAM_0 if self.team == 0 else COLOR_TEAM_1
        has_ball_color = COLOR_WITH_BALL if self.has_ball else COLOR_WITHOUT_BALL
        return base_color, has_ball_color
