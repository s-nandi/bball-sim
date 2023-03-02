from typing import List, Iterable, Optional, Union
from bball.player import Player
from bball.team import Team, Teams


def _normalized_teams(teams: List[Team]) -> Teams:
    assert len(teams) <= 2
    while len(teams) <= 2:
        teams.append(Team())
    return Teams(teams[0], teams[1])


Players = Union[Optional[Iterable[Player]], Player]


def create_team(players: Players = None) -> Team:
    if players is None:
        players = []
    if isinstance(players, Player):
        return Team(players)
    return Team(*players)


def create_teams(team_1: Players = None, team_2: Players = None) -> Teams:
    teams = [create_team(players) for players in [team_1, team_2]]
    return _normalized_teams(teams)
