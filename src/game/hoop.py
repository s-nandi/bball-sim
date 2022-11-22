import dataclasses
import time
from typing import Iterable, Optional
import pygame
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.draw import draw_circle, SCORE_INDICATOR_DURATION_SEC
from game.colors import BASKETBALL_COLOR, BLACK


@dataclasses.dataclass
class Hoop(PhysicsObject):
    body: pymunk.Body
    shape: pymunk.Shape
    time_scored_on: Optional[float] = None

    def __init__(self, radius, position):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.sensor = True

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield self.shape

    def draw(self, screen: pygame.Surface, scale: float):
        self.check_unscore()
        color = BASKETBALL_COLOR if self.was_scored_on else BLACK
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

    @property
    def was_scored_on(self) -> bool:
        return self.time_scored_on is not None

    def score(self):
        self.time_scored_on = time.monotonic()

    def check_unscore(self):
        if not self.time_scored_on:
            return
        if time.monotonic() - self.time_scored_on >= SCORE_INDICATOR_DURATION_SEC:
            self.time_scored_on = None
