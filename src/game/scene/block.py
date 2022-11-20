from typing import List, Tuple
import pymunk


class Block:
    body: pymunk.Body
    shape: pymunk.Shape

    def __init__(self, size: float, position: pymunk.Vec2d, mass: float):
        points = self.create_points(size)
        self.body = self.create_body(mass, points, position)
        self.shape = self.create_shape(self.body, points)

    @staticmethod
    def create_points(size) -> List[Tuple[float, float]]:
        return [
            (-size, -size),
            (-size, size),
            (size, size),
            (size, -size),
        ]

    @staticmethod
    def create_body(mass, points, position) -> pymunk.Body:
        moment = pymunk.moment_for_poly(mass, points)
        body = pymunk.Body(mass, moment)
        body.position = position
        return body

    @staticmethod
    def create_shape(body, points) -> pymunk.Shape:
        shape = pymunk.Poly(body, points)
        shape.friction = 1
        return shape
