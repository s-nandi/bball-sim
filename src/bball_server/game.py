from typing import List, Tuple, Callable, Optional
from dataclasses import dataclass, field
from random import random
from bball_server.ball import BallMode, Ball
from bball_server.court import Court, Hoop
from bball_server.player import Player
from bball_server.utils import close_to
from bball_server.validator import valid_shot_value

Team = List[Player]
Teams = Tuple[Team, Team]
MonitoringFunction = Callable[[], bool]
Score = Tuple[float, float]


def other_team(team_index: int) -> int:
    return 1 - team_index


@dataclass
class ScoreBoard:
    _score_1: float = 0
    _score_2: float = 0

    @property
    def score(self) -> Score:
        return (self._score_1, self._score_2)

    def increment(self, team_index: int, value: float):
        assert valid_shot_value(value)
        if team_index == 0:
            self._score_1 += value
        elif team_index == 1:
            self._score_2 += value
        else:
            assert False, f"Invalid team index {team_index}, must be 0 or 1"


@dataclass
class GameSettings:
    use_expected_value_for_points: bool = False


@dataclass
class Game:
    teams: Teams
    ball: Ball
    court: Court
    settings: GameSettings = field(default_factory=GameSettings)
    _scoreboard: ScoreBoard = field(init=False, default_factory=ScoreBoard)

    @property
    def _checks(self) -> List[MonitoringFunction]:
        return [
            self.check_out_of_bounds,
            self.arbitrary_inbound,
            self.transfer_posession,
            self.potentially_make_basket,
        ]

    def _step(self, _time_frame: float) -> bool:
        for check in self._checks:
            if check():
                return True
        return False

    def team_index_of(self, player: Player) -> int:
        for team_index, team in enumerate(self.teams):
            if team.count(player) > 0:
                return team_index
        assert False, f"Player {player} does not exist in game"

    @property
    def score(self) -> Score:
        return self._scoreboard.score

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
        if self.ball.mode != BallMode.RECEIVEDPASS:
            return False
        self.ball.successful_pass(self.ball.passed_to)
        return True

    def _determine_if_score_and_apply_score_change(self) -> bool:
        assert self.ball.mode == BallMode.REACHEDSHOT
        shot = self.ball.shot_parameters
        player = shot.shooter
        team = self.team_index_of(player)
        target_hoop = self.target_hoop(player)
        assert close_to(shot.target, target_hoop.position)
        value = target_hoop.value_of_shot_from(shot.location)
        if self.settings.use_expected_value_for_points:
            self._scoreboard.increment(team, shot.probability * value)
            return True
        print(shot.probability)
        made_shot = random() < shot.probability
        if made_shot:
            self._scoreboard.increment(team, value)
        return made_shot

    def potentially_make_basket(self) -> bool:
        if self.ball.mode != BallMode.REACHEDSHOT:
            return False
        if self._determine_if_score_and_apply_score_change():
            self.ball.successful_shot()
            return True
        self.ball.missed_shot()
        return True
