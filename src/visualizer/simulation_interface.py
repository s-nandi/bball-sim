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

    @abstractmethod
    def draw(self, screen: pygame.Surface, scale: float) -> None:
        pass

    def pre_draw(self, screen: pygame.Surface) -> None:
        pymunk.pygame_util.positive_y_is_up = True
        screen.fill(pygame.Color("white"))

    def post_draw(self) -> None:
        pygame.display.flip()

    def complete_draw(self, screen: pygame.Surface, scale: float) -> None:
        self.pre_draw(screen)
        self.draw(screen, scale)
        self.post_draw()
