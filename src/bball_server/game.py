from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass
from bball_server.ball import BallMode, Ball
from bball_server.court import Court
from bball_server.player import Player

Team = List[Player]
Teams = Tuple[Team, Team]
MonitoringFunction = Callable[[], bool]


def other_team(team_index: int) -> int:
    return 1 - team_index


@dataclass
class Game:
    teams: Teams
    ball: Ball
    court: Court

    @property
    def _checks_per_mode(self) -> Dict[BallMode, List[MonitoringFunction]]:
        return {
            BallMode.HELD: [self.check_out_of_bounds],
            BallMode.DEAD: [self.arbitrary_inbound],
        }

    def _step(self, _time_frame: float):
        checks = self._checks_per_mode.get(self.ball.mode, [])
        for check in checks:
            if check():
                return

    def team_index_of(self, player: Player):
        for team_index, team in enumerate(self.teams):
            if team.count(player) > 0:
                return team_index
        assert False, f"Player {player} does not exist in game"

    @property
    def team_with_last_posession(self) -> Optional[int]:
        last_ball_handler = self.ball.last_belonged_to
        if last_ball_handler is None:
            return None
        return self.team_index_of(last_ball_handler)

    def check_out_of_bounds(self) -> bool:
        if self.court.is_inbounds(self.ball):
            return False
        self.ball.held_out_of_bounds()
        return True

    def arbitrary_inbound(self) -> bool:
        team_with_posession = (
            self.team_with_last_posession
            if self.team_with_last_posession is not None
            else 0
        )
        new_team_with_posession = (
            team_with_posession
            if not self.ball.should_flip_posession
            else other_team(team_with_posession)
        )
        player = self.teams[new_team_with_posession][0]
        if not self.court.is_inbounds(player):
            return False
        self.ball.jump_ball_won_by(player)
        return True
