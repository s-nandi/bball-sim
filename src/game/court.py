import dataclasses
from typing import Iterable, List
import pymunk
from physics_lib import PhysicsObject, PhysicsComponent
from game.utils import rotate
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


@dataclasses.dataclass
class CourtDimensions:
    width: float
    height: float
    boundary_thickness: float

    @property
    def x_min(self) -> float:
        return self.boundary_thickness

    @property
    def x_max(self) -> float:
        return self.width - self.boundary_thickness

    @property
    def y_min(self) -> float:
        return self.boundary_thickness

    @property
    def y_max(self) -> float:
        return self.height - self.boundary_thickness


class Court(PhysicsObject):
    dimensions: CourtDimensions
    boundaries: List[Boundary]

    def __init__(self, dimensions: CourtDimensions):
        self.dimensions = dimensions
        self.boundaries = self.create_boundaries(dimensions)

    def physics_components(self) -> Iterable[PhysicsComponent]:
        for boundary in self.boundaries:
            yield from boundary.physics_components()

    @staticmethod
    def create_boundaries(dimensions: CourtDimensions) -> List[Boundary]:
        boundaries = []
        endpoints = [
            (dimensions.x_min, dimensions.y_max),
            (dimensions.x_max, dimensions.y_max),
            (dimensions.x_max, dimensions.y_min),
            (dimensions.x_min, dimensions.y_min),
        ]
        boundaries = [
            Boundary(endpoint_1, endpoint_2, dimensions.boundary_thickness)
            for endpoint_1, endpoint_2 in zip(endpoints, rotate(endpoints))
        ]
        return boundaries
