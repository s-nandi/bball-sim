from typing import List
import pygame
from visualizer.renderer import Renderer
from visualizer.simulator import Simulator
from visualizer.screen_params import ScreenParams
from visualizer.types import SpeedScale
from visualizer.game_interface import GameInterface


def should_keep_running(events: List[pygame.event.Event]) -> bool:
    for event in events:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True


class Visualizer:
    renderer: Renderer
    simulation: Simulator
    game: GameInterface
    events: List[pygame.event.Event]

    def __init__(
        self,
        screen_params: ScreenParams,
        game: GameInterface,
        simulation_speed_scale: SpeedScale,
    ):
        self.renderer = Renderer(screen_params)
        self.simulation = Simulator(
            game.getspace(), screen_params.fps, simulation_speed_scale
        )
        self.game = game
        self.events = []

    def run(self) -> None:
        self.game.initialize()
        while should_keep_running(self.events):
            self.loop()

    def loop(self) -> None:
        self.events = pygame.event.get()
        self.game.update()
        self.simulation.step()
        self.renderer.render(self.simulation)
