from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Type, TypeVar, Any
from bball_server.utils import coords_to_string, Point
from bball_server.ball.ball_mode import BallMode
from bball_server.ball.server import _Server
from bball_server.ball.held_ball_server import _HeldBallServer
from bball_server.ball.mid_pass_server import _MidPassServer
from bball_server.ball.post_pass_server import _PostPassServer
from bball_server.ball.mid_shot_server import _MidShotServer
from bball_server.ball.post_shot_server import _PostShotServer
from bball_server.ball.dead_ball_server import _DeadBallServer


if TYPE_CHECKING:
    from bball_server.player import Player

T = TypeVar("T")


def _checked(server: Any, variable_type: Type[T]) -> T:
    assert isinstance(server, variable_type)
    return server


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
        return _checked(self._server, _DeadBallServer)._should_flip_posession

    @property
    def shot_parameters(self) -> _PostShotServer:
        return _checked(self._server, _PostShotServer)

    @property
    def passed_to(self) -> Player:
        return _checked(self._server, _PostPassServer)._receiver

    @property
    def belongs_to(self) -> Player:
        return _checked(self._server, _HeldBallServer)._ball_handler

    def _step(self, time_frame: float) -> bool:
        return self._server._step(time_frame)

    def _transition(self, previous_server_type: Type[_Server], server: _Server) -> Ball:
        _checked(self._server, previous_server_type)._reset()
        self._server = server
        return self

    def held_out_of_bounds(self):
        return self._transition(_HeldBallServer, _DeadBallServer(True))

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        return self._transition(
            _HeldBallServer,
            _MidPassServer(self.belongs_to, receiver, self, pass_velocity),
        )

    def shoot_at(self, target: Point, shot_velocity: float) -> Ball:
        return self._transition(
            _HeldBallServer,
            _MidShotServer(self.belongs_to, target, self, shot_velocity),
        )

    def post_pass(self, receiver: Player) -> Ball:
        return self._transition(_MidPassServer, _PostPassServer(receiver))

    def successful_pass(self, receiver: Player) -> Ball:
        return self._transition(_PostPassServer, _HeldBallServer(receiver, self))

    def post_shot(self, shooter: Player, target: Point, shot_from: Point) -> Ball:
        return self._transition(
            _MidShotServer, _PostShotServer(shooter, target, shot_from)
        )

    def successful_shot(self) -> Ball:
        return self._transition(_PostShotServer, _DeadBallServer(True))

    def jump_ball_won_by(self, receiver: Player) -> Ball:
        return self._transition(_DeadBallServer, _HeldBallServer(receiver, self))
