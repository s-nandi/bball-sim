from game import Game
from visualizer import Visualizer, ScreenParams


def setup_simulation() -> Visualizer:
    screen_params = ScreenParams(width=600, height=800, fps=30)
    game = Game()
    simulation = Visualizer(
        screen_params,
        game,
        simulation_speed_scale=0.2,
    )
    return simulation


def main() -> None:
    simulation = setup_simulation()
    simulation.run()


if __name__ == "__main__":
    main()
