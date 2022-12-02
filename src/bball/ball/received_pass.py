from dataclasses import dataclass
from bball.player import Player
from bball.ball.state import BallState
from bball.ball.ball_mode import BallMode


@dataclass
class ReceivedPass(BallState):
    _receiver: Player

    @staticmethod
    def mode() -> BallMode:
        return BallMode.RECEIVEDPASS
