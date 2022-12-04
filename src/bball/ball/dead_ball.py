from dataclasses import dataclass
from bball.ball.state import BallState
from bball.ball.ball_mode import BallMode


@dataclass
class DeadBall(BallState):
    _should_flip_possession: bool

    @staticmethod
    def mode() -> BallMode:
        return BallMode.DEAD
