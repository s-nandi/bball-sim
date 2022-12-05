from __future__ import annotations
from typing import List, Callable, Optional
from dataclasses import dataclass, field
from random import random
from bball.ball import BallMode, Ball
from bball.court import Court, Hoop, HalfCourt
from bball.player import Player
from bball.utils import close_to
from bball.game.scoreboard import Scoreboard
from bball.team import Team, Teams, other_team_index
from bball.strategy import StrategyInterface

MonitoringFunction = Callable[[], bool]
TimedMonitoringFunction = Callable[[float], bool]


@dataclass
class GameSettings:
    shot_clock_duration: float = float("inf")
    use_expected_value_for_points: bool = False
    use_instant_inbounding: bool = True


@dataclass
class ShotClock:
    shot_clock_duration: float
    possession_time: float = field(init=False, default=0.0)
    active_possession: Optional[int] = field(init=False, default=None)

    def __post_init__(self):
        self.possession_ended()

    def did_expire_after_step(self, time_frame: float) -> bool:
        self.possession_time -= time_frame
        self.possession_time = max(0, self.possession_time)
        if self.active_possession is None:
            return False
        return self.possession_time <= 0.0

    def possession_ended(self):
        self.possession_time = self.shot_clock_duration
        self.active_possession = None

    def possession_started(self, team_index: int) -> bool:
        if self.active_possession != team_index:
            self.possession_time = self.shot_clock_duration
            self.active_possession = team_index
            return True
        return False


@dataclass
class Game:
    teams: Teams
    ball: Ball
    court: Court
    settings: GameSettings = field(default_factory=GameSettings)
    _scoreboard: Scoreboard = field(init=False, default_factory=Scoreboard)
    _clock: ShotClock = field(init=False)

    def __post_init__(self):
        self._clock = ShotClock(self.settings.shot_clock_duration)

    def assign_team_strategy(
        self, team_index: int, strategy: StrategyInterface
    ) -> Game:
        strategy.for_team_index_in_game(team_index, self)
        self.teams[team_index]._strategy = strategy
        return self

    @property
    def _checks(self) -> List[MonitoringFunction]:
        return [
            self.check_out_of_bounds,
            self.arbitrary_inbound,
            self.transfer_possession,
            self.potentially_make_basket,
        ]

    @property
    def _timed_checks(self) -> List[TimedMonitoringFunction]:
        return [self.check_shot_clock]

    def _step(self, time_frame: float) -> bool:
        for timed_check in self._timed_checks:
            if timed_check(time_frame):
                return True
        for check in self._checks:
            if check():
                return True
        return False

    def team_index_of(self, player: Player) -> int:
        for team_index, team in enumerate(self.teams):
            assert isinstance(team, Team)
            if player in team:
                return team_index
        assert False, f"Player {player} does not exist in game"

    @property
    def shot_clock(self) -> float:
        return self._clock.possession_time

    @property
    def scoreboard(self) -> Scoreboard:
        return self._scoreboard

    @property
    def team_with_last_possession(self) -> Optional[int]:
        last_ball_handler = self.ball.last_belonged_to
        if last_ball_handler is None:
            return None
        return self.team_index_of(last_ball_handler)

    def target_hoop(self, player: Player) -> Hoop:
        team_index = self.team_index_of(player)
        return self.court._hoops[other_team_index(team_index)]

    def target_half_court(self, player: Player) -> HalfCourt:
        team_index = self.team_index_of(player)
        return self.court.half_court(other_team_index(team_index))

    def check_shot_clock(self, time_frame: float) -> bool:
        if self.ball.mode in [BallMode.DEAD, BallMode.MIDSHOT, BallMode.REACHEDSHOT]:
            self._clock.possession_ended()
        else:
            team_with_possession = self.team_with_last_possession
            assert team_with_possession is not None
            if self._clock.possession_started(team_with_possession):
                self._scoreboard.increment_possessions(team_with_possession)
        if self._clock.did_expire_after_step(time_frame):
            self.ball.shot_clock_expired()
            return True
        return False

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
        team_with_possession = (
            self.team_with_last_possession
            if self.team_with_last_possession is not None
            else 0
        )
        new_team_with_possession = (
            team_with_possession
            if not self.ball.should_flip_possession
            else other_team_index(team_with_possession)
        )

        if self.settings.use_instant_inbounding:
            player = self.teams[new_team_with_possession][0]
            if not self.court.is_inbounds(player):
                return False
            self.ball.jump_ball_won_by(player)
            return True

        for team_index, team in enumerate(self.teams):
            has_possession = team_index == new_team_with_possession
            inbounding_data = team.reset_on_inbound(has_possession)
            if has_possession:
                self.ball.jump_ball_won_by(team[inbounding_data.player_with_ball])
            half_court = self.court.half_court(team_index)
            positions = inbounding_data.positions_for_half_court(half_court)
            if team_index == 1:
                positions = reversed(positions)
            base_orientation = 0 if team_index == 0 else -180
            orientations = [
                base_orientation + delta for delta in inbounding_data.orientation_deltas
            ]
            for player, position, orientation in zip(team, positions, orientations):
                player.place_at(position, orientation)
        return True

    def transfer_possession(self) -> bool:
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
            self._scoreboard.increment_score(team, shot.probability * value)
            return True
        made_shot = random() < shot.probability
        if made_shot:
            self._scoreboard.increment_score(team, value)
        return made_shot

    def potentially_make_basket(self) -> bool:
        if self.ball.mode != BallMode.REACHEDSHOT:
            return False
        if self._determine_if_score_and_apply_score_change():
            self.ball.successful_shot()
            return True
        self.ball.missed_shot()
        return True
