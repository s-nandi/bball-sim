from __future__ import annotations
from typing import TYPE_CHECKING
from bball_server.ball.ball_mode import BallMode

if TYPE_CHECKING:
    from bball_server.player import Player
    from bball_server.ball import Ball


class _HeldBallServer:
    _ball_handler: Player
    _ball: Ball

    def __init__(self, receiver: Player, ball: Ball):
        self._ball_handler = receiver
        self._ball = ball
        receiver._ball = ball
        ball._last_belonged_to = receiver
        ball._position = receiver.position

    def _step(self, _time_frame: float) -> bool:
        self._ball._position = self._ball_handler.position
        return False

    def _reset(self):
        self._ball_handler._ball = None

    @staticmethod
    def mode() -> BallMode:
        return BallMode.HELD
