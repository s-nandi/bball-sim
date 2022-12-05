from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from time import monotonic
from bball.game import Game, Scoreboard
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
    allowed_distance_off_court: float = float("inf")
    _max_distance: float = field(init=False, default=0.0)
    _start_time: Optional[float] = field(init=False, default=None)
    _simulation_time: float = field(init=False, default=0.0)
    _last_scoreboard: Scoreboard = field(init=False, default_factory=Scoreboard)

    @property
    def simulationtime(self) -> float:
        return self._simulation_time

    @property
    def runtime(self) -> float:
        if self._start_time is None:
            return 0.0
        current_time = monotonic()
        return current_time - self._start_time

    @property
    def max_distance(self) -> float:
        return self._max_distance

    def stats(self) -> Dict[str, Any]:
        def format_float(value: float) -> float:
            return round(value, 2)

        score = self._last_scoreboard.score
        return {
            "max_distance": format_float(self.max_distance),
            "runtime": format_float(self.runtime),
            "simulationtime": self.simulationtime,
            "score": (
                format_float(score[0]),
                format_float(score[1]),
            ),
            "possessions": self._last_scoreboard.possessions,
        }

    def monitor(self, game: Game, time_frame: float):
        if self._start_time is None:
            self._start_time = monotonic()
        monitor_bounds(game, self.allowed_distance_off_court)
        distance = monitor_distance(game)
        self._max_distance = max(self._max_distance, distance)
        self._last_scoreboard = game.scoreboard
        self._simulation_time += time_frame
