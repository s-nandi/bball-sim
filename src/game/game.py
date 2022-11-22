from typing import List, Iterable, Callable
import pygame
import pymunk
import pymunk.pygame_util
from visualizer.simulation_interface import SimulationInterface
from physics_lib import PhysicsObject, PhysicsComponent
from game.player import Player
from game.court import Court


class Game(SimulationInterface, PhysicsObject):
    players: List[Player]
    court: Court
    space: pymunk.Space
    player_behavior: Callable

    def __init__(
        self,
        players: List[Player],
        court: Court,
        player_behavior: Callable,
    ):
        self.space = pymunk.Space()
        self.players = players
        self.court = court
        self.player_behavior = player_behavior
        self.players[0].has_ball = True

    def physics_components(self) -> Iterable[PhysicsComponent]:
        for player in self.players:
            yield from player.physics_components()
        yield from self.court.physics_components()

    def getspace(self) -> pymunk.Space:
        return self.space

    def draw(self, screen: pygame.Surface, scale: float) -> None:
        self.court.draw(screen, scale)
        for player in self.players:
            player.draw(screen, scale)

    def initialize(self) -> None:
        self.space.damping = self.court.damping
        self.add_to_space(self.space)

    def update(self) -> None:
        self.player_behavior(self.players, self.court)
