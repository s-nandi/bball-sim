from typing import Tuple, Callable
import pygame
from engine.render_settings import RenderSettings


class Engine:
    surface: pygame.surface.Surface
    clock: pygame.time.Clock
    render_settings: RenderSettings

    def __init__(self, resolution: Tuple[int, int], frame_rate: int):
        pygame.init()
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.render_settings = RenderSettings(resolution, frame_rate)

    def run(self, callback: Callable[[], None]):
        while self.should_loop():
            self.surface.fill((255, 255, 255))
            callback()
            self.clock.tick(self.render_settings.frame_rate)
            pygame.display.set_caption(str(round(self.clock.get_fps(), 2)))
            pygame.display.flip()
        pygame.quit()

    def should_loop(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True
