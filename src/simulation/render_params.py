import pygame
import pymunk
import pymunk.pygame_util
from simulation.screen_params import ScreenParams
from simulation.types import Fps


class RenderParams:
    screen: pygame.Surface
    fps: Fps
    clock: pygame.time.Clock
    draw_options: pymunk.pygame_util.DrawOptions

    def __init__(self, screen_params: ScreenParams):
        self.screen = pygame.display.set_mode(
            (screen_params.width, screen_params.height)
        )  # type: ignore
        self.fps = screen_params.fps
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
