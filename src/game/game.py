import itertools
from typing import List
import logging
import pymunk
from visualizer.simulation_interface import SimulationInterface
from game.player import Player, generate_players


def create_players() -> List[Player]:
    players = generate_players(
        mass_generator=itertools.repeat(0.1),
        size_generator=itertools.repeat(10.0),
        max_speed_generator=itertools.cycle([43.0, 30.0]),
        max_acceleration_generator=itertools.cycle([50.0, 90.0]),
        position_generator=[(150, 150), (200, 200)],
    )
    return list(players)


class Game(SimulationInterface):
    players: List[Player]
    space: pymunk.Space

    def __init__(self):
        self.space = pymunk.Space()
        self.players = create_players()

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
