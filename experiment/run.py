from bball.initiate import two_uniform_players
from bball.strategy import DoNothing, RunToBasketAndShoot
from bball.create import create_strategy
from bball.game import Game
from runner import run_game


def monitor(game: Game):
    player_1 = game.teams[0][0]
    assert 0 <= player_1.position[0] <= game.court.width


def main():
    game = two_uniform_players()
    game.assign_team_strategy(0, create_strategy(5))
    game.assign_team_strategy(1, create_strategy(3))
    run_game(game, fps=60, callback=lambda: monitor(game))


if __name__ == "__main__":
    main()
