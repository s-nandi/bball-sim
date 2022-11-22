from typing import List, Iterable, Callable
import pygame
import pymunk
import pymunk.pygame_util
from visualizer.simulation_interface import SimulationInterface
from physics_lib import PhysicsObject, PhysicsComponent
from game.player import Player
from game.court import Court
from game.draw import draw_court_markings, draw_circle, Color


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

    def physics_components(self) -> Iterable[PhysicsComponent]:
        for player in self.players:
            yield from player.physics_components()
        yield from self.court.physics_components()

    def getspace(self) -> pymunk.Space:
        return self.space

    def draw(self, screen: pygame.Surface, scale: float = 1.0) -> None:
        draw_court_markings(self.court.dimensions, screen, scale)
        draw_circle(
            screen,
            self.court.dimensions.left_rim_position,
            radius=10.0,
            thickness=0.1,
            outline_color=Color(255, 0, 0, 255),
            subdivisions=20,
            scale=scale,
        )
        draw_circle(
            screen,
            self.court.dimensions.right_rim_position,
            radius=10.0,
            thickness=0.1,
            outline_color=Color(255, 0, 0, 255),
            subdivisions=20,
            scale=scale,
        )
        SimulationInterface.draw(self, screen, scale)

    def initialize(self) -> None:
        self.space.damping = self.court.damping
        self.add_to_space(self.space)

    def update(self) -> None:
        self.player_behavior(self.players, self.court)
