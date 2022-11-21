from abc import ABC, abstractmethod
import pymunk
import pygame


class SimulationInterface(ABC):
    @abstractmethod
    def getspace(self) -> pymunk.Space:
        pass

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    def pre_draw(self, screen: pygame.Surface) -> None:
        pymunk.pygame_util.positive_y_is_up = True
        screen.fill(pygame.Color("white"))

    def draw(self, screen: pygame.Surface, scale: float = 1.0) -> None:
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        draw_options.transform = pymunk.Transform.scaling(scale)
        self.getspace().debug_draw(draw_options)

    def post_draw(self) -> None:
        pygame.display.flip()

    def complete_draw(self, screen: pygame.Surface, scale: float = 1.0) -> None:
        self.pre_draw(screen)
        self.draw(screen, scale)
        self.post_draw()
