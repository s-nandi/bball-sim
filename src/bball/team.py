from typing import List, Tuple
from bball.player import Player


class Team:
    _players: List[Player]

    def __init__(self, *players: Player):
        self._players = list(players)

    def __iter__(self):
        return iter(self._players)

    def __contains__(self, player: Player):
        return player in self._players

    def __getitem__(self, index):
        return self._players.__getitem__(index)


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
