import math
import pygame
import pymunk
import pymunk.pygame_util
from visualizer.types import TimePerFrame, Fps, SpeedScale
from visualizer.game_interface import GameInterface


class Simulator:
    game: GameInterface
    time_per_frame: TimePerFrame

    @classmethod
    def max_allowable_step(cls) -> TimePerFrame:
        return 0.01

    def __init__(
        self,
        game: GameInterface,
        fps: Fps,
        speed_scale: SpeedScale = 1.0,
    ):
        self.game = game
        self.time_per_frame = speed_scale / fps

    @property
    def space(self) -> pymunk.Space:
        return self.game.getspace()

    def initialize(self) -> None:
        self.game.initialize()

    def step(self) -> None:
        self.game.update()
        substeps = math.ceil(max(1, self.time_per_frame / self.max_allowable_step()))
        for _ in range(substeps):
            self.space.step(self.time_per_frame / substeps)

    def draw(self, screen: pygame.Surface) -> None:
        pymunk.pygame_util.positive_y_is_up = True
        screen.fill(pygame.Color("white"))
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(screen))
        pygame.display.flip()
