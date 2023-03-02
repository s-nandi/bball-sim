from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, TYPE_CHECKING
from bball.validator import valid_positive_multiplier

if TYPE_CHECKING:
    from bball.player import Player
    from bball.strategy import StrategyInterface
    from bball.utils import Point
    from bball.court import HalfCourt


@dataclass
class InboundData:
    player_with_ball: int
    position_multipliers: List[Point]
    orientation_deltas: List[float]

    def __post_init__(self):
        for position_multiplier in self.position_multipliers:
            assert valid_positive_multiplier(position_multiplier[0])
            assert valid_positive_multiplier(position_multiplier[1])

    def positions_for_half_court(self, half_court: HalfCourt):
        return [
            half_court.multiplier_to_position(multiplier)
            for multiplier in self.position_multipliers
        ]


class Team:
    _players: List[Player]
    _strategy: Optional[StrategyInterface] = None

    def __init__(self, *players: Player):
        self._players = list(players)

    def __iter__(self):
        return iter(self._players)

    def __len__(self):
        return len(self._players)

    def __contains__(self, player: Player):
        return player in self._players

    def __getitem__(self, index):
        return self._players.__getitem__(index)

    def reset_on_inbound(self, given_possession: bool) -> InboundData:
        player_with_ball = 0 if given_possession else -1
        positions = [
            (0.1, (i + 1) / (len(self._players) + 1))
            for i, _ in enumerate(self._players)
        ]
        orientations = [0.0] * len(self._players)
        return InboundData(player_with_ball, positions, orientations)


class Teams:
    _teams: Tuple[Team, Team]

    def __init__(self, *teams: Team):
        assert len(teams) == 2
        self._teams = (teams[0], teams[1])

    def __getitem__(self, index):
        return self._teams.__getitem__(index)

    def __iter__(self):
        return iter(self._teams)


def other_team_index(team_index: int) -> int:
    return 1 - team_index
