from runner import run_game
from experiment.monitor import Monitor
from experiment import initiate


def main():
    game = initiate.players_collision()

    monitor = Monitor()
    run_game(game, fps=60, monitor=lambda: monitor.monitor(game))
    print("max dist", monitor.max_distance)


if __name__ == "__main__":
    main()
