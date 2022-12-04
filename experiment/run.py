from runner import run_game
from experiment.monitor import Monitor
from experiment import initiate


def main():
    game = initiate.tests.setup_stay_relatively_on_court_with_composite_strategy(1.0)

    monitor = Monitor(1.0)
    run_game(game, fps=60, monitor=lambda: monitor.monitor(game))
    print("max dist", monitor.max_distance)
    print("duration", monitor.time_since_start)


if __name__ == "__main__":
    main()
