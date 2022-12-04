from pprint import pprint
from runner import run_game
from experiment.monitor import Monitor
from experiment import initiate


def main():
    game = initiate.players_collision()

    monitor = Monitor(float("inf"))
    run_game(game, fps=60, display_scale=0.3, monitor=lambda: monitor.monitor(game))
    pprint(monitor.stats())


if __name__ == "__main__":
    main()
