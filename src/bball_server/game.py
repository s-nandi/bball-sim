from typing import List, Tuple, Callable, Optional
from dataclasses import dataclass
from bball_server.ball import BallMode, Ball
from bball_server.court import Court, Hoop
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
    def _checks(self) -> List[MonitoringFunction]:
        return [
            self.check_out_of_bounds,
            self.arbitrary_inbound,
            self.transfer_posession,
            self.score_basket,
        ]

    def _step(self, _time_frame: float) -> bool:
        for check in self._checks:
            if check():
                return True
        return False

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

    def target_hoop(self, player: Player) -> Hoop:
        team_index = self.team_index_of(player)
        return self.court._hoops[other_team(team_index)]

    def check_out_of_bounds(self) -> bool:
        if self.ball.mode != BallMode.HELD:
            return False
        if self.court.is_inbounds(self.ball):
            return False
        self.ball.held_out_of_bounds()
        return True

    def arbitrary_inbound(self) -> bool:
        if self.ball.mode != BallMode.DEAD:
            return False
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

    def transfer_posession(self) -> bool:
        if self.ball.mode != BallMode.POSTPASS:
            return False
        self.ball.successful_pass(self.ball.passed_to)
        return True

    def score_basket(self) -> bool:
        if self.ball.mode != BallMode.POSTSHOT:
            return False
        self.ball.successful_shot()
        return True
