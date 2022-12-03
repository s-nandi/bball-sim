from dataclasses import dataclass
from bball.game import Game
from bball.player import Player
from bball.utils import distance_between


def monitor_bounds(game: Game, threshold: float):
    def check_player(player: Player):
        assert -threshold <= player.position[0] <= game.court.width + threshold
        assert -threshold <= player.position[1] <= game.court.height + threshold

    for team in game.teams:
        for player in team:
            check_player(player)


def monitor_distance(game: Game):
    global max_distance
    distance = distance_between(game.teams[0][0].position, game.teams[1][0].position)
    return distance


@dataclass
class Monitor:
    max_distance: float = 0.0

    def monitor(self, game: Game):
        monitor_bounds(game, 1.0)
        distance = monitor_distance(game)
        self.max_distance = max(self.max_distance, distance)
