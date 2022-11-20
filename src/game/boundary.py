from typing import Iterable
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.types import ConvertibleToVec2d, convert_to_vec2d


class Boundary(PhysicsObject):
    body: pymunk.Body
    shape: pymunk.Shape

    def __init__(
        self,
        endpoint_1: ConvertibleToVec2d,
        endpoint_2: ConvertibleToVec2d,
        thickness: float,
    ):
        endpoint_1 = convert_to_vec2d(endpoint_1)
        endpoint_2 = convert_to_vec2d(endpoint_2)

        self.body = self.create_body()
        self.shape = self.create_shape(endpoint_1, endpoint_2, self.body, thickness)

    def physics_components(self) -> Iterable[PhysicsComponent]:
        yield self.body
        yield self.shape

    @staticmethod
    def create_body() -> pymunk.Body:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        return body

    @staticmethod
    def create_shape(
        endpoint_1: pymunk.Vec2d,
        endpoint_2: pymunk.Vec2d,
        body: pymunk.Body,
        radius: float,
    ) -> pymunk.Segment:
        segment = pymunk.Segment(body, endpoint_1, endpoint_2, radius)
        return segment
