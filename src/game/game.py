import random
import pymunk
from simulation.game_interface import GameInterface
from game.scene import SceneObjects


class Game(GameInterface):
    scene: SceneObjects

    def __init__(self):
        self.scene = SceneObjects()

    def initialize(self, space: pymunk.Space) -> None:
        space.gravity = (0.0, -900.0)
        space.sleep_time_threshold = 0.3
        for obj in self.scene.objects():
            space.add(obj)

    def update(self, space: pymunk.Space) -> None:
        ground = self.scene.ground
        blocks = self.scene.blocks
        choice = random.randrange(3)
        if choice == 0:
            up_force = pymunk.Vec2d(0, 10000)
            body = ground.body
            body.apply_impulse_at_local_point(up_force)
        elif choice == 1:
            if self.scene.blocks:
                removed_block = blocks.pop(random.randrange(len(blocks)))
                space.remove(removed_block.body, removed_block.shape)
        elif choice == 2:
            if self.scene.blocks:
                up_impulse = pymunk.Vec2d(0, 1000)
                body = random.choice(self.scene.blocks).body
                body.apply_impulse_at_local_point(up_impulse)
        else:
            assert False
