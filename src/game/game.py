import itertools
from typing import List
import logging
import pymunk
from visualizer.simulation_interface import SimulationInterface
from game.scene import Player, PlayerAttributes


def create_players() -> List[Player]:
    masses = itertools.repeat(0.1)
    sizes = itertools.repeat(10.0)
    max_speeds = [43.0, 30.0]
    max_accelerations = [50.0, 90.0]
    positions = (pymunk.Vec2d(*p) for p in [(150, 150), (200, 200)])
    return [
        Player(
            PlayerAttributes(
                mass=mass,
                size=size,
                max_speed=max_speed,
                max_acceleration=max_acceleration,
            ),
            position,
        )
        for mass, size, max_speed, max_acceleration, position in zip(
            masses, sizes, max_speeds, max_accelerations, positions
        )
    ]


class Game(SimulationInterface):
    players: List[Player]
    space: pymunk.Space

    def __init__(self):
        self.space = pymunk.Space()
        self.players = create_players()
        self.first = True

    def getspace(self) -> pymunk.Space:
        return self.space

    def initialize(self) -> None:
        self.space.sleep_time_threshold = 0.3
        for player in self.players:
            player.add_to_space(self.space)

    def update(self) -> None:
        for player in self.players:
            player.move(pymunk.Vec2d(1, 0), 100)
            logging.info(player)
