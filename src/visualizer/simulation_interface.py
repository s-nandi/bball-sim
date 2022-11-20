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

    def draw(self, screen: pygame.Surface) -> None:
        pymunk.pygame_util.positive_y_is_up = True
        screen.fill(pygame.Color("white"))
        self.getspace().debug_draw(pymunk.pygame_util.DrawOptions(screen))
        pygame.display.flip()
