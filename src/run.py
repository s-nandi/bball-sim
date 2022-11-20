import logging
from game import Game
from visualizer import Visualizer, ScreenParams


def configure_logger() -> None:
    logging.basicConfig(filename="output/run.log", level=logging.DEBUG)


def setup_simulation() -> Visualizer:
    screen_params = ScreenParams(width=800, height=600, fps=30)
    game = Game()
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
