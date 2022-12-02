from typing import Type
from bball.game import Game
from bball.team import Team
from bball.strategy.strategy_interface import StrategyInterface


class CompositeStrategy:
    team: Team
    offensive_strategy: StrategyInterface
    defensive_strategy: StrategyInterface

    def __init__(
        self,
        team: Team,
        offensive_strategy_type: Type[StrategyInterface],
        defensive_strategy_type: Type[StrategyInterface],
        time_frame: float,
        *,
        offensive_strategy_params=None,
        defensive_strategy_params=None,
    ):
        if offensive_strategy_params is None:
            offensive_strategy_params = {}
        if defensive_strategy_params is None:
            defensive_strategy_params = {}

        self.team = team
        self.offensive_strategy = offensive_strategy_type(
            team, time_frame, **offensive_strategy_params
        )
        self.defensive_strategy = defensive_strategy_type(
            team, time_frame, *defensive_strategy_params
        )

    def drive(self, game: Game):
        offensive_team_index = game.team_with_last_posession
        if offensive_team_index is None:
            return
        if self.team == game.teams[offensive_team_index]:
            self.offensive_strategy.drive(game)
        else:
            self.defensive_strategy.drive(game)
