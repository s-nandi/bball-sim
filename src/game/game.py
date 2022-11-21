from typing import List, Iterable
import logging
import pygame
import pymunk
import pymunk.pygame_util
from visualizer.simulation_interface import SimulationInterface
from physics_lib import PhysicsObject, PhysicsComponent
from game.player import Player
from game.court import Court
from game.draw import draw_court_markings


class Game(SimulationInterface, PhysicsObject):
    players: List[Player]
    court: Court
    space: pymunk.Space

    def __init__(self, players: List[Player], court: Court):
        self.space = pymunk.Space()
        self.players = players
        self.court = court

    def physics_components(self) -> Iterable[PhysicsComponent]:
        for player in self.players:
            yield from player.physics_components()
        yield from self.court.physics_components()

    def getspace(self) -> pymunk.Space:
        return self.space

    def initialize(self) -> None:
        self.space.sleep_time_threshold = 0.3
        self.add_to_space(self.space)

    def update(self) -> None:
        for player in self.players:
            player.move((1, 0), 100)
            logging.info(player)

    def draw(self, screen: pygame.Surface, scale: float = 1.0) -> None:
        draw_court_markings(self.court.dimensions, screen, scale)
        SimulationInterface.draw(self, screen, scale)
