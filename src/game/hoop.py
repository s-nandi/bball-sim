import dataclasses
from typing import Iterable
import pygame
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.draw import Color, draw_circle


@dataclasses.dataclass
class Hoop(PhysicsObject):
    body: pymunk.Body
    shape: pymunk.Shape

    def __init__(self, radius, position):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.sensor = True

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield self.shape

    def draw(self, screen: pygame.Surface, scale: float):
        color = Color(30, 30, 30, 255)
        radius = self.shape.radius
        thickness = 8
        draw_circle(
            screen,
            self.body.position,
            radius=radius,
            fill_color=color,
            thickness=thickness,
            scale=scale,
        )
