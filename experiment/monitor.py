from dataclasses import dataclass, field
from typing import Optional
from time import monotonic
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
    distance = distance_between(game.teams[0][0].position, game.teams[1][0].position)
    return distance


@dataclass
class Monitor:
    allowed_distance_off_court: float = 1.0
    max_distance: float = field(init=False, default=0.0)
    _start_time: Optional[float] = field(init=False, default=None)

    @property
    def time_since_start(self) -> float:
        if self._start_time is None:
            return 0.0
        current_time = monotonic()
        return current_time - self._start_time

    def monitor(self, game: Game):
        if self._start_time is None:
            self._start_time = monotonic()
        monitor_bounds(game, self.allowed_distance_off_court)
        distance = monitor_distance(game)
        self.max_distance = max(self.max_distance, distance)
