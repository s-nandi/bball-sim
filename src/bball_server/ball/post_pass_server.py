from dataclasses import dataclass
from bball_server.player import Player


@dataclass
class _PostPassServer:
    _receiver: Player
