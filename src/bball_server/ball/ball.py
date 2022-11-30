from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Union
from bball_server.utils import coords_to_string, Point
from bball_server.ball.ball_mode import BallMode
from bball_server.ball.held_ball_server import _HeldBallServer
from bball_server.ball.mid_pass_server import _MidPassServer
from bball_server.ball.post_pass_server import _PostPassServer
from bball_server.ball.mid_shot_server import _MidShotServer
from bball_server.ball.post_shot_server import _PostShotServer
from bball_server.ball.dead_ball_server import _DeadBallServer


if TYPE_CHECKING:
    from bball_server.player import Player


_Server = Union[
    _HeldBallServer,
    _MidPassServer,
    _PostPassServer,
    _MidShotServer,
    _PostShotServer,
    _DeadBallServer,
]


class Ball:
    _position: Point
    _last_belonged_to: Optional[Player]
    _server: _Server

    def __init__(self):
        self._position = (0, 0)
        self._last_belonged_to = None
        self._server = _DeadBallServer(False)

    def __repr__(self):
        return (
            f"Ball(position = {coords_to_string(self._position)}, mode = {self.mode})"
        )

    @property
    def position(self) -> Point:
        return self._position

    @property
    def mode(self) -> BallMode:
        return self._server.mode()

    @property
    def last_belonged_to(self) -> Optional[Player]:
        return self._last_belonged_to

    @property
    def should_flip_posession(self) -> bool:
        assert self.mode == BallMode.DEAD
        server = self._server
        assert isinstance(server, _DeadBallServer)
        return server._should_flip_posession

    @property
    def shot_parameters(self) -> _PostShotServer:
        assert self.mode == BallMode.POSTSHOT
        server = self._server
        assert isinstance(server, _PostShotServer)
        return server

    @property
    def passed_to(self) -> Player:
        assert self.mode == BallMode.POSTPASS
        server = self._server
        assert isinstance(server, _PostPassServer)
        return server._receiver

    @property
    def belongs_to(self) -> Player:
        server = self._server
        assert isinstance(server, _HeldBallServer)
        return server._ball_handler

    def _step(self, time_frame: float) -> bool:
        if self.mode in [BallMode.POSTPASS, BallMode.POSTSHOT, BallMode.DEAD]:
            return False
        if self.mode in [BallMode.HELD, BallMode.MIDPASS, BallMode.MIDSHOT]:
            server = self._server
            assert isinstance(server, (_MidShotServer, _MidPassServer, _HeldBallServer))
            return server._step(time_frame)
        assert False, f"Invalid ball mode {self.mode}"

    def _reset(self) -> None:
        if self.mode == BallMode.HELD:
            server = self._server
            assert isinstance(server, _HeldBallServer)
            server._reset()
        elif self.mode in [
            BallMode.MIDPASS,
            BallMode.MIDSHOT,
            BallMode.POSTSHOT,
            BallMode.DEAD,
            BallMode.POSTPASS,
        ]:
            pass
        else:
            assert False

    def held_out_of_bounds(self):
        assert self.mode == BallMode.HELD
        self._reset()
        self._server = _DeadBallServer(True)
        return self

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        assert self.mode == BallMode.HELD
        self._reset()
        self._server = _MidPassServer(self.belongs_to, receiver, self, pass_velocity)
        return self

    def shoot_at(self, target: Point, shot_velocity: float) -> Ball:
        assert self.mode == BallMode.HELD
        self._reset()
        self._server = _MidShotServer(self.belongs_to, target, self, shot_velocity)
        return self

    def post_pass(self, receiver: Player) -> Ball:
        assert self.mode == BallMode.MIDPASS
        self._reset()
        self._server = _PostPassServer(receiver)
        return self

    def successful_pass(self, receiver: Player) -> Ball:
        assert self.mode == BallMode.POSTPASS
        self._reset()
        self._server = _HeldBallServer(receiver, self)
        return self

    def post_shot(self, shooter: Player, target: Point, shot_from: Point) -> Ball:
        assert self.mode == BallMode.MIDSHOT
        self._reset()
        self._server = _PostShotServer(shooter, target, shot_from)
        return self

    def successful_shot(self) -> Ball:
        assert self.mode == BallMode.POSTSHOT
        self._reset()
        self._server = _DeadBallServer(True)
        return self

    def jump_ball_won_by(self, receiver: Player) -> Ball:
        assert self.mode == BallMode.DEAD
        self._reset()
        self._server = _HeldBallServer(receiver, self)
        return self
