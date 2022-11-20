import pymunk
from visualizer.simulation_interface import SimulationInterface


class Game(SimulationInterface):
    space: pymunk.Space

    def __init__(self):
        self.space = pymunk.Space()

    def getspace(self) -> pymunk.Space:
        return self.space

    def initialize(self) -> None:
        pass

    def update(self) -> None:
        pass
