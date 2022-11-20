import pymunk

from game.utils import zero_gravity


class Ground:
    body: pymunk.Body
    shape: pymunk.Shape

    def __init__(
        self,
        mass: float,
        left_endpoint: pymunk.Vec2d,
        right_endpoint: pymunk.Vec2d,
        friction: float = 1.0,
    ):
        self.body = self.create_body(mass, left_endpoint, right_endpoint)
        self.shape = self.create_ground(
            left_endpoint, right_endpoint, friction, self.body
        )

    @staticmethod
    def create_body(
        mass: float,
        left_endpoint: pymunk.Vec2d,
        right_endpoint: pymunk.Vec2d,
        radius: float = 1.0,
        position: pymunk.Vec2d = pymunk.Vec2d(0, 0),
    ) -> pymunk.Body:
        moment = pymunk.moment_for_segment(mass, left_endpoint, right_endpoint, radius)
        body = pymunk.Body(mass, moment, pymunk.Body.DYNAMIC)
        body.position = position
        body.velocity_func = zero_gravity
        return body

    @staticmethod
    def create_ground(
        left_endpoint: pymunk.Vec2d,
        right_endpoint: pymunk.Vec2d,
        friction: float,
        body: pymunk.Body,
        radius: float = 1.0,
    ) -> pymunk.Segment:
        ground = pymunk.Segment(body, left_endpoint, right_endpoint, radius)
        ground.friction = friction
        return ground
