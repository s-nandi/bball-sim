from typing import Tuple
import pygame
from visualizer.screen_params import ScreenParams
from visualizer.types import Fps
from visualizer.simulation_interface import SimulationInterface

DISPLAY_SCALE = 0.95


def scale_while_maintaining_resolution(
    max_w: float, max_h: float, target_w_to_h: float
) -> Tuple[float, float]:
    max_scale = min(max_w / target_w_to_h, max_h / 1)
    return (max_scale * target_w_to_h, max_scale)


class Engine:
    screen: pygame.Surface
    screen_params: ScreenParams
    target_fps: Fps
    clock: pygame.time.Clock

    def __init__(self, screen_params: ScreenParams):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            scale_while_maintaining_resolution(
                display_info.current_w * DISPLAY_SCALE,
                display_info.current_h * DISPLAY_SCALE,
                screen_params.width / screen_params.height,
            )
        )  # type: ignore
        self.screen.fill(pygame.Color("white"))

        self.screen_params = screen_params
        self.target_fps = screen_params.fps
        self.clock = pygame.time.Clock()

    def tick(self) -> float:
        self.clock.tick(self.target_fps)
        return round(self.clock.get_fps(), 2)

    def render(self, simulation: SimulationInterface):
        screen_rect = self.screen.get_rect()
        buffer = pygame.Surface(screen_rect.size)
        scale_factor = min(
            screen_rect.width / self.screen_params.width,
            screen_rect.height / self.screen_params.height,
        )
        simulation.draw(buffer, scale_factor)
        self.screen.blit(buffer, (0, 0))
        caption = f"fps: {str(self.tick())}"
        pygame.display.set_caption(caption)
