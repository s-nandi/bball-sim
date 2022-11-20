from typing import List, Iterator, Union
import pymunk
from game.scene.ground import Ground
from game.scene.block import Block

PymunkObj = Union[pymunk.Body, pymunk.Shape, pymunk.Constraint]


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

    def objects(self) -> Iterator[PymunkObj]:
        yield self.ground.body
        yield self.ground.shape
        for block in self.blocks:
            yield block.body
            yield block.shape
