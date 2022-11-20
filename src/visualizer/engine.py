import pygame
from visualizer.screen_params import ScreenParams
from visualizer.types import Fps
from visualizer.simulation_interface import SimulationInterface

DISPLAY_SCALE = 0.80


class Engine:
    screen: pygame.Surface
    surface: pygame.Surface
    target_fps: Fps
    clock: pygame.time.Clock

    def __init__(self, screen_params: ScreenParams):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (
                display_info.current_w * DISPLAY_SCALE,
                display_info.current_h * DISPLAY_SCALE,
            )
        )  # type: ignore
        self.screen.fill(pygame.Color("white"))

        self.surface = pygame.Surface((screen_params.width, screen_params.height))
        self.target_fps = screen_params.fps
        self.clock = pygame.time.Clock()

    def tick(self) -> float:
        self.clock.tick(self.target_fps)
        return round(self.clock.get_fps(), 2)

    def render(self, simulation: SimulationInterface):
        simulation.draw(self.surface)
        screen_rect = self.screen.get_rect()
        surface_rect = self.surface.get_rect(center=screen_rect.center)
        self.screen.blit(self.surface, surface_rect)
        caption = f"fps: {str(self.tick())}"
        pygame.display.set_caption(caption)
