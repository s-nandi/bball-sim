from pprint import pprint
from runner import run_game
from experiment.monitor import Monitor
from experiment import initiate


def main():
    game = initiate.tests.setup_consistent_inbounds_despite_collisions(True)

    monitor = Monitor(float("inf"))
    run_game(game, fps=60, display_scale=0.3, monitor=lambda: monitor.monitor(game))
    pprint(monitor.stats())


if __name__ == "__main__":
    main()
