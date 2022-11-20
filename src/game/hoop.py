import dataclasses
from typing import Iterable
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent


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
