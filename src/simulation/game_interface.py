from abc import ABC, abstractmethod
import pymunk


class GameInterface(ABC):
    @abstractmethod
    def initialize(self, space: pymunk.Space) -> None:
        pass

    @abstractmethod
    def update(self, space: pymunk.Space) -> None:
        pass
