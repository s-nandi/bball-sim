from bball.initiate import two_uniform_players
from bball.strategy import DoNothing, RunToBasketAndShoot
from runner import run_game


def main():
    game = two_uniform_players()
    game.assign_team_strategy(0, RunToBasketAndShoot(5))
    game.assign_team_strategy(1, DoNothing())
    run_game(game, fps=30)


if __name__ == "__main__":
    main()
