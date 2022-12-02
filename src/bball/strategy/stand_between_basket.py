from dataclasses import dataclass, field
from typing import List
from bball.game import Game
from bball.player import Player
from bball.team import Team, other_team_index
from bball.behavior import StandBetween
from bball.strategy.strategy_interface import StrategyInterface


@dataclass
class StandBetweenBasket(StrategyInterface):
    team: Team
    time_frame: float
    _have_matchups: bool = field(init=False, default=False)
    _behaviors: List[StandBetween] = field(init=False)
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
            self._behaviors[player_index] = StandBetween(
                matchup, target_hoop, self.time_frame
            )
        for behavior, player in zip(self._behaviors, self.team):
            behavior.drive(player)
