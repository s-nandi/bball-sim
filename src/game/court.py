from typing import Iterable, List
import pygame
from physics_lib import PhysicsObject, PhysicsComponent
from game.utils import rotate
from game.dimensions import CourtDimensions
from game.boundary import Boundary
from game.hoop import Hoop
from game.draw import draw_court_markings


class Court(PhysicsObject):
    dimensions: CourtDimensions
    boundaries: List[Boundary]
    hoops: List[Hoop]
    damping: float

    def __init__(self, dimensions: CourtDimensions, damping: float):
        self.dimensions = dimensions
        self.boundaries = self.create_boundaries(dimensions)
        self.hoops = self.create_hoops(dimensions)
        self.damping = damping

    def physics_components(self) -> Iterable[PhysicsComponent]:
        for boundary in self.boundaries:
            yield from boundary.physics_components()
        for hoop in self.hoops:
            yield from hoop.physics_components()

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

    @staticmethod
    def create_hoops(dimensions: CourtDimensions) -> List[Hoop]:
        positions = [dimensions.left_rim_position, dimensions.right_rim_position]
        return [Hoop(dimensions.rim.radius, position) for position in positions]

    def draw(self, screen: pygame.Surface, scale: float):
        draw_court_markings(self.dimensions, screen, scale)
        for hoop in self.hoops:
            hoop.draw(screen, scale)
