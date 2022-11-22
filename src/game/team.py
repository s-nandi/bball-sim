from typing import List, Tuple
from game.player import Player
from game.types import Team


TEAMS: Tuple[Team, Team] = (0, 1)


def other_team(team: Team) -> Team:
    return 0 if team == 1 else 1


def split_by_team(players: List[Player]) -> Tuple[List[Player], List[Player]]:
    res: Tuple[List[Player], List[Player]] = ([], [])
    for team in TEAMS:
        for player in players:
            if player.team == team:
                res[team].append(player)
    return res
