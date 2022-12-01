from typing import List, Tuple
from bball_server.player import Player


class Team:
    players: List[Player]

    def __init__(self, *players: Player):
        self.players = list(players)

    def __iter__(self):
        return iter(self.players)

    def contains(self, player: Player):
        return self.players.count(player) > 0

    def random_player(self):
        assert len(self.players) > 0
        return self.players[0]


Teams = Tuple[Team, Team]


def other_team_index(team_index: int) -> int:
    return 1 - team_index
