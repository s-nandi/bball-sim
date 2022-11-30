from __future__ import annotations
from enum import Enum, auto
from typing import Optional, TYPE_CHECKING, Union
from bball_server.utils import coords_to_string, Point
from bball_server.ball.passing_server import _PassingServer
from bball_server.ball.shooting_server import _ShootingServer
from bball_server.ball.scoring_server import _ScoringServer
from bball_server.ball.dead_ball_server import _DeadBallServer
from bball_server.ball.post_pass_server import _PostPassServer
from bball_server.ball.held_ball_server import _HeldBallServer


if TYPE_CHECKING:
    from bball_server.player import Player


class BallMode(Enum):
    MIDPASS = auto()
    POSTPASS = auto()
    HELD = auto()
    DEAD = auto()
    MIDSHOT = auto()
    POSTSHOT = auto()


_Server = Union[
    _PassingServer,
    _ShootingServer,
    _ScoringServer,
    _DeadBallServer,
    _PostPassServer,
    _HeldBallServer,
]


class Ball:
    _position: Point
    _belongs_to: Optional[Player]
    _last_belonged_to: Optional[Player]
    _server: Optional[_Server]
    _mode: BallMode

    def __init__(self):
        self._position = (0, 0)
        self._last_belonged_to = None
        self._server = _DeadBallServer(False)
        self._mode = BallMode.DEAD

    def __repr__(self):
        return (
            f"Ball(position = {coords_to_string(self._position)}, mode = {self._mode})"
        )

    @property
    def position(self) -> Point:
        return self._position

    @property
    def mode(self) -> BallMode:
        return self._mode

    @property
    def last_belonged_to(self) -> Optional[Player]:
        return self._last_belonged_to

    @property
    def should_flip_posession(self) -> bool:
        assert self._mode == BallMode.DEAD
        server = self._unsafe_server()
        assert isinstance(server, _DeadBallServer)
        return server._should_flip_posession

    @property
    def shot_parameters(self) -> _ScoringServer:
        assert self._mode == BallMode.POSTSHOT
        server = self._unsafe_server()
        assert isinstance(server, _ScoringServer)
        return server

    @property
    def passed_to(self) -> Player:
        assert self._mode == BallMode.POSTPASS
        server = self._unsafe_server()
        assert isinstance(server, _PostPassServer)
        return server._receiver

    @property
    def belongs_to(self) -> Player:
        server = self._unsafe_server()
        assert isinstance(server, _HeldBallServer)
        return server._ball_handler

    def _unsafe_server(self) -> _Server:
        assert self._server is not None
        return self._server

    def _step(self, time_frame: float) -> bool:
        if self._mode in [BallMode.POSTPASS, BallMode.POSTSHOT, BallMode.DEAD]:
            return False
        if self._mode in [BallMode.HELD, BallMode.MIDPASS, BallMode.MIDSHOT]:
            server = self._unsafe_server()
            assert isinstance(
                server, (_ShootingServer, _PassingServer, _HeldBallServer)
            )
            return server._step(time_frame)
        assert False, f"Invalid ball mode {self._mode}"

    def _reset(self) -> None:
        if self._mode == BallMode.HELD:
            server = self._unsafe_server()
            assert isinstance(server, _HeldBallServer)
            server._reset()
        elif self._mode in [
            BallMode.MIDPASS,
            BallMode.MIDSHOT,
            BallMode.POSTSHOT,
            BallMode.DEAD,
            BallMode.POSTPASS,
        ]:
            pass
        else:
            assert False

    def _with_mode(self, mode: BallMode) -> Ball:
        self._mode = mode
        return self

    def held_out_of_bounds(self):
        assert self._mode == BallMode.HELD
        self._reset()
        self._server = _DeadBallServer(True)
        return self._with_mode(BallMode.DEAD)

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        assert self._mode == BallMode.HELD
        self._reset()
        self._server = _PassingServer(self.belongs_to, receiver, self, pass_velocity)
        return self._with_mode(BallMode.MIDPASS)

    def shoot_at(self, target: Point, shot_velocity: float) -> Ball:
        assert self._mode == BallMode.HELD
        self._reset()
        self._server = _ShootingServer(self.belongs_to, target, self, shot_velocity)
        return self._with_mode(BallMode.MIDSHOT)

    def post_pass(self, receiver: Player) -> Ball:
        assert self._mode == BallMode.MIDPASS
        self._reset()
        self._server = _PostPassServer(receiver)
        return self._with_mode(BallMode.POSTPASS)

    def successful_pass(self, receiver: Player) -> Ball:
        assert self._mode == BallMode.POSTPASS
        self._reset()
        self._server = _HeldBallServer(receiver, self)
        return self._with_mode(BallMode.HELD)

    def post_shot(self, shooter: Player, target: Point, shot_from: Point) -> Ball:
        assert self._mode == BallMode.MIDSHOT
        self._reset()
        self._server = _ScoringServer(shooter, target, shot_from)
        return self._with_mode(BallMode.POSTSHOT)

    def successful_shot(self) -> Ball:
        assert self._mode == BallMode.POSTSHOT
        self._reset()
        self._server = _DeadBallServer(True)
        return self._with_mode(BallMode.DEAD)

    def jump_ball_won_by(self, receiver: Player) -> Ball:
        assert self._mode == BallMode.DEAD
        self._reset()
        self._server = _HeldBallServer(receiver, self)
        return self._with_mode(BallMode.HELD)
