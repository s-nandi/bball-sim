from dataclasses import dataclass, field
from typing import Optional, List, Union
from bball.game import Game
from bball.player import Player
from bball.team import Team, other_team_index
from bball.behavior import (
    ReachPositionBehavior,
    RunPastPositionBehavior,
    StopBehavior,
)
from bball.utils import (
    distance_between,
    midpoint_of,
    sum_of,
    same_direction_as,
)


class OffensiveStrategy:
    def drive(self, game: Game):
        pass


@dataclass
class EveryoneRunToBasketStrategy(OffensiveStrategy):
    distance_threshold: float
    time_frame: float
    team: Team
    _behaviors: List[Optional[ReachPositionBehavior]] = field(init=False)

    def __post_init__(self):
        self._behaviors = [None for _ in self.team]

    def drive(self, game: Game):
        for player_index, player in enumerate(self.team):
            target_hoop = game.target_hoop(player)
            if self._behaviors[player_index] is None:
                self._behaviors[player_index] = ReachPositionBehavior(
                    target_hoop.position, self.time_frame
                )

        for behavior, player in zip(self._behaviors, self.team):
            close_enough = (
                distance_between(player.position, target_hoop.position)
                <= self.distance_threshold
            )
            if player.has_ball and close_enough:
                player.shoot_at(target_hoop.position, 1)
            else:
                assert behavior is not None
                behavior.drive(player)


class DefensiveStrategy:
    def drive(self, game: Game):
        pass


@dataclass
class StandBetweenBasket(DefensiveStrategy):
    team: Team
    time_frame: float
    _have_matchups: bool = field(init=False, default=False)
    _behaviors: List[Union[StopBehavior, RunPastPositionBehavior]] = field(init=False)
    _opponent_team: Team = field(init=False)
    _matchups: List[Player] = field(init=False)

    def __post_init__(self):
        self._behaviors = [None for _ in self.team]
        self._opponent_team = []
        self._matchups = []

    def _initialize_matchups(self, game: Game):
        if self._have_matchups:
            return
        for player in self.team:
            team_index = game.team_index_of(player)
            self._opponent_team = game.teams[other_team_index(team_index)]
        self._matchups = list(self._opponent_team)

    def drive(self, game: Game):
        self._initialize_matchups(game)
        index_player = enumerate(self.team)
        for (player_index, player), matchup in zip(index_player, self._matchups):
            target_hoop = game.target_hoop(matchup)
            projected_matchup_position = sum_of(matchup.position, matchup.velocity)
            midpoint = midpoint_of(target_hoop.position, projected_matchup_position)
            already_in_front = same_direction_as(
                target_hoop.position, player.position, midpoint
            )
            if already_in_front:
                self._behaviors[player_index] = StopBehavior(self.time_frame)
            else:
                self._behaviors[player_index] = RunPastPositionBehavior(
                    midpoint, self.time_frame
                )
        for behavior, player in zip(self._behaviors, self.team):
            behavior.drive(player)


@dataclass
class Strategy:
    offensive_strategy: OffensiveStrategy
    defensive_strategy: DefensiveStrategy

    def drive(self, team: Team, game: Game):
        offensive_team_index = game.team_with_last_posession
        assert offensive_team_index is not None
        if team == game.teams[offensive_team_index]:
            self.offensive_strategy.drive(game)
        else:
            self.defensive_strategy.drive(game)
