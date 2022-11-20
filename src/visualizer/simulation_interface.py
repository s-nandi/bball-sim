from abc import ABC, abstractmethod
import pymunk


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
