from typing import List
import pygame
from visualizer.engine import Engine
from visualizer.simulator import Simulator
from visualizer.screen_params import ScreenParams
from visualizer.types import SpeedScale
from visualizer.simulation_interface import SimulationInterface


def should_keep_running(events: List[pygame.event.Event]) -> bool:
    for event in events:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True


class Visualizer:
    engine: Engine
    simulator: Simulator
    events: List[pygame.event.Event]

    def __init__(
        self,
        screen_params: ScreenParams,
        simulation: SimulationInterface,
        simulation_speed_scale: SpeedScale,
    ):
        self.engine = Engine(screen_params)
        self.simulator = Simulator(
            simulation, screen_params.fps, simulation_speed_scale
        )
        self.events = []

    @property
    def simulation(self):
        return self.simulator.simulation

    def run(self) -> None:
        self.simulator.initialize()
        while should_keep_running(self.events):
            self.loop()

    def loop(self) -> None:
        self.events = pygame.event.get()
        self.simulator.step()
        self.engine.render(self.simulation)
