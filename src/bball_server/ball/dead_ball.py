from dataclasses import dataclass
from bball_server.ball.state import BallState
from bball_server.ball.ball_mode import BallMode


@dataclass
class DeadBall(BallState):
    _should_flip_posession: bool

    @staticmethod
    def mode() -> BallMode:
        return BallMode.DEAD
