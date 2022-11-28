from typing import List, Tuple
from dataclasses import dataclass
from bball_server.player import Player
from bball_server.ball import Ball, BallMode
from bball_server.court import Court

Team = List[Player]
Teams = Tuple[Team, Team]


@dataclass
class Game:
    teams: Teams
    ball: Ball
    court: Court

    def _step(self, _time_frame: float):
        if self.ball.mode == BallMode.HELD:
            self.check_out_of_bounds()
        else:
            pass

    def check_out_of_bounds(self):
        if not self.court.is_inbounds(self.ball):
            self.ball.held_out_of_bounds()
