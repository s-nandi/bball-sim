from dataclasses import dataclass
from bball_server.player import Player
from bball_server.ball.state import BallState
from bball_server.ball.ball_mode import BallMode


@dataclass
class ReceivedPass(BallState):
    _receiver: Player

    @staticmethod
    def mode() -> BallMode:
        return BallMode.RECEIVEDPASS
