from bball.initiate import two_uniform_players
from bball.strategy import DoNothing, RunToBasketAndShoot
from bball.create import create_strategy
from runner import run_game


def main():
    game = two_uniform_players()
    game.assign_team_strategy(0, create_strategy(5))
    game.assign_team_strategy(1, create_strategy(3))
    run_game(game, fps=60)


if __name__ == "__main__":
    main()
