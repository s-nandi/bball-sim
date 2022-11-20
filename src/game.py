import dataclasses
from typing import List, Tuple, Iterator, Union
import random
import pymunk
from simulation import ScreenParams, Simulator, PymunkObj, InitializeFn, UpdateFn

PymunkObj = Union[pymunk.Body, pymunk.Shape, pymunk.Constraint]


def zero_gravity(body, _gravity, damping, d_time):
    pymunk.Body.update_velocity(body, (0, 0), damping, d_time)


@dataclasses.dataclass
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


@dataclasses.dataclass
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


class SceneObjects:
    ground: Ground
    blocks: List[Block]

    def __init__(self):
        self.ground = self.create_ground()
        self.blocks = self.create_pyramid()

    @staticmethod
    def create_ground() -> Ground:
        mass = 1000
        left_endpoint = pymunk.Vec2d(0, 100)
        right_endpoint = pymunk.Vec2d(600, 100)
        friction = 1.0
        ground = Ground(mass, left_endpoint, right_endpoint, friction)
        return ground

    @staticmethod
    def create_pyramid() -> List[Block]:
        blocks = []
        size = 10.0
        mass = 1.0
        xpos = pymunk.Vec2d(-270, 7.5) + (300, 100)
        ypos = pymunk.Vec2d(0, 0)
        delta_x = pymunk.Vec2d(0.5625, 1.1) * 20
        delta_y = pymunk.Vec2d(1.125, 0.0) * 20
        for i in range(25):
            ypos = pymunk.Vec2d(*xpos)
            for _ in range(i, 25):
                blocks.append(Block(size, ypos, mass))
                ypos += delta_y
            xpos += delta_x
        return blocks

    def __iter__(self) -> Iterator[PymunkObj]:
        ret: List[PymunkObj] = []
        ret.append(self.ground.body)
        ret.append(self.ground.shape)
        for block in self.blocks:
            ret.append(block.body)
            ret.append(block.shape)
        return ret.__iter__()

    def attach_ground_to_body(self, body: pymunk.Body) -> None:
        self.ground.shape.body = body

    def initializer(self) -> InitializeFn:
        def initialize(space: pymunk.Space) -> None:
            space.gravity = (0.0, -900.0)
            space.sleep_time_threshold = 0.3
            for obj in self:
                space.add(obj)

        return initialize

    def updater(self) -> UpdateFn:
        def update(space: pymunk.Space) -> None:
            choice = random.randrange(3)
            if choice == 0:
                if self.ground:
                    up_force = pymunk.Vec2d(0, 10000)
                    body = self.ground.body
                    body.apply_impulse_at_local_point(up_force)
            elif choice == 1:
                if self.blocks:
                    removed_block = self.blocks.pop(random.randrange(len(self.blocks)))
                    space.remove(removed_block.body, removed_block.shape)
            elif choice == 2:
                if self.blocks:
                    up_impulse = pymunk.Vec2d(0, 1000)
                    body = random.choice(self.blocks).body
                    body.apply_impulse_at_local_point(up_impulse)
            else:
                assert False

        return update


def setup_simulation() -> Simulator:
    scene_objects = SceneObjects()
    simulation = Simulator(
        ScreenParams(width=600, height=800, fps=30),
        scene_objects.initializer(),
        scene_objects.updater(),
        simulation_speed_scale=0.2,
    )
    return simulation


def main() -> None:
    simulation = setup_simulation()
    simulation.run()


if __name__ == "__main__":
    main()
