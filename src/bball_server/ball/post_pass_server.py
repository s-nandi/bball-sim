from dataclasses import dataclass
from bball_server.player import Player
from bball_server.ball.server import _Server
from bball_server.ball.ball_mode import BallMode


@dataclass
class _PostPassServer(_Server):
    _receiver: Player

    @staticmethod
    def mode() -> BallMode:
        return BallMode.POSTPASS
