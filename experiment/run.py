from bball.initiate import two_uniform_players
from bball.create import create_strategy
from bball.game import Game
from bball.player import Player
from runner import run_game


def monitor(game: Game):
    threshold = 1

    def check_player(player: Player):
        assert -threshold <= player.position[0] <= game.court.width + threshold
        assert -threshold <= player.position[1] <= game.court.height + threshold

    check_player(game.teams[0][0])
    check_player(game.teams[1][0])


def main():
    game = two_uniform_players()
    game.assign_team_strategy(0, create_strategy(0.01))
    game.assign_team_strategy(1, create_strategy(0.01))
    run_game(game, fps=60, monitor=lambda: monitor(game))


if __name__ == "__main__":
    main()
