from pprint import pprint
from runner import run_game
from experiment.monitor import Monitor
from experiment import initiate


def main():
    game = initiate.multiple_players(2)

    monitor = Monitor(float("inf"))
    run_game(
        game,
        fps=90,
        speed_scale=5.0,
        display_scale=0.3,
        monitor=lambda: monitor.monitor(game),
    )
    pprint(monitor.stats())


if __name__ == "__main__":
    main()
