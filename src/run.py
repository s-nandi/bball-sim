from game import Game
from simulation import Simulator, ScreenParams


def setup_simulation() -> Simulator:
    game = Game()
    simulation = Simulator(
        ScreenParams(width=600, height=800, fps=30),
        game,
        simulation_speed_scale=0.2,
    )
    return simulation


def main() -> None:
    simulation = setup_simulation()
    simulation.run()


if __name__ == "__main__":
    main()
