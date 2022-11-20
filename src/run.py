import itertools
import logging
from typing import List
from game import Game, Player, generate_players, Court, CourtDimensions
from visualizer import Visualizer, ScreenParams


def configure_logger() -> None:
    logging.basicConfig(filename="output/run.log", level=logging.DEBUG)


def create_players() -> List[Player]:
    players = generate_players(
        mass_generator=itertools.cycle([0.1, 1]),
        size_generator=itertools.repeat(5.0),
        max_speed_generator=itertools.cycle([60.0, 40.0]),
        max_acceleration_generator=itertools.cycle([50.0, 130.0]),
        position_generator=[(10, 10), (30, 30)],
    )
    return list(players)


def create_court(width: float, height: float) -> Court:
    return Court(CourtDimensions(width, height, boundary_thickness=1.0))


def setup_simulation() -> Visualizer:
    width = 450
    height = 250
    screen_params = ScreenParams(width=width, height=height, fps=30)
    game = Game(create_players(), create_court(width, height))
    simulation = Visualizer(
        screen_params,
        game,
        simulation_speed_scale=1.0,
    )
    return simulation


def main() -> None:
    configure_logger()
    simulation = setup_simulation()
    simulation.run()


if __name__ == "__main__":
    main()
