from bball.initiate import two_uniform_players
from bball.create import create_strategy

from runner import run_game
from experiment.monitor import Monitor


def main():
    game = two_uniform_players()
    game.assign_team_strategy(0, create_strategy(0.01))
    game.assign_team_strategy(1, create_strategy(20))

    monitor = Monitor()
    run_game(game, fps=60, monitor=lambda: monitor.monitor(game))
    print("max dist", monitor.max_distance)


if __name__ == "__main__":
    main()
