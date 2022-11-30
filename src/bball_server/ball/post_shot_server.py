from dataclasses import dataclass
from bball_server.player import Player
from bball_server.utils import Point
from bball_server.ball.ball_mode import BallMode


@dataclass
class _PostShotServer:
    shooter: Player
    target: Point
    location: Point

    @staticmethod
    def mode() -> BallMode:
        return BallMode.POSTSHOT
