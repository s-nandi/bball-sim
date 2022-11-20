import pygame
from visualizer.screen_params import ScreenParams
from visualizer.types import Fps
from visualizer.simulation_interface import SimulationInterface


class Engine:
    screen: pygame.Surface
    target_fps: Fps
    clock: pygame.time.Clock

    def __init__(self, screen_params: ScreenParams):
        self.screen = pygame.display.set_mode(
            (screen_params.width, screen_params.height)
        )  # type: ignore
        self.target_fps = screen_params.fps
        self.clock = pygame.time.Clock()

    def tick(self) -> float:
        self.clock.tick(self.target_fps)
        return round(self.clock.get_fps(), 2)

    def render(self, simulation: SimulationInterface):
        simulation.draw(self.screen)
        caption = f"fps: {str(self.tick())}"
        pygame.display.set_caption(caption)
