from dataclasses import dataclass
from bball_server.ball.ball_mode import BallMode


@dataclass
class _DeadBallServer:
    _should_flip_posession: bool

    @staticmethod
    def mode() -> BallMode:
        return BallMode.DEAD
