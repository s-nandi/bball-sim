from pprint import pprint
from runner import run_game
from experiment.monitor import Monitor
from experiment import initiate


def main():
    game = initiate.tests.setup_collision_with_use_behavior(7, 2.0, 1.0)

    monitor = Monitor(float("inf"))
    run_game(game, fps=60, monitor=lambda: monitor.monitor(game))
    pprint(monitor.stats())


if __name__ == "__main__":
    main()
