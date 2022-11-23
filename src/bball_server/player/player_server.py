import uuid
from typing import Dict
from bball_server.player.player import Player
from bball_server.player.player_attributes import PlayerAttributes

PlayerId = str


def generate_id():
    return str(uuid.uuid1())[:8]


class PlayerServer:
    players: Dict[PlayerId, Player]

    def __init__(self):
        self.players = {}

    def create_player(self, attributes: PlayerAttributes) -> PlayerId:
        player_id = generate_id()
        self.players[player_id] = Player(attributes)
        return player_id

    def get_player(self, player_id: PlayerId) -> Player:
        player = self.players.get(player_id)
        if player is None:
            assert False
        return player
