from __future__ import annotations
from enum import Enum, auto
from typing import Optional, TYPE_CHECKING, Union
from bball_server.utils import coords_to_string, Point
from bball_server.ball.passing_server import _PassingServer
from bball_server.ball.shooting_server import _ShootingServer

if TYPE_CHECKING:
    from bball_server.player import Player


class BallMode(Enum):
    MIDPASS = auto()
    POSTPASS = auto()
    HELD = auto()
    DEAD = auto()
    MIDSHOT = auto()
    POSTSHOT = auto()


_TERMINAL_MODES = [BallMode.POSTPASS, BallMode.POSTSHOT, BallMode.DEAD]
_Server = Union[_PassingServer, _ShootingServer]


class Ball:
    _position: Point
    _belongs_to: Optional[Player]
    _last_belonged_to: Optional[Player]
    _server: Optional[_Server]
    _passed_to: Optional[Player]
    _should_flip_posession: Optional[bool]
    _mode: BallMode

    def __init__(self):
        self._position = (0, 0)
        self._belongs_to = None
        self._last_belonged_to = None
        self._server = None
        self._passed_to = None
        self._mode = BallMode.DEAD
        self._should_flip_posession = None

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
        assert self._should_flip_posession is not None
        return self._should_flip_posession

    @property
    def passed_to(self) -> Player:
        assert self._mode == BallMode.POSTPASS
        assert self._passed_to is not None
        return self._passed_to

    def _unsafe_belongs_to(self) -> Player:
        assert self._belongs_to is not None
        return self._belongs_to

    def _unsafe_server(self) -> _Server:
        assert self._server is not None
        return self._server

    def _give_posession(self, player: Player) -> None:
        self._belongs_to = player
        self._unsafe_belongs_to()._ball = self
        self._last_belonged_to = player

    def _remove_posession(self) -> None:
        self._unsafe_belongs_to()._ball = None
        self._belongs_to = None

    def _step(self, time_frame: float) -> bool:
        if self._mode in _TERMINAL_MODES:
            return False
        if self._mode == BallMode.HELD:
            self._position = self._unsafe_belongs_to().position
            return False
        if self._mode in [BallMode.MIDPASS, BallMode.MIDSHOT]:
            return self._unsafe_server()._step(time_frame)
        assert False, f"Invalid ball mode {self._mode}"

    def _reset(self) -> None:
        if self.mode == BallMode.DEAD:
            self._should_flip_posession = None
        elif self.mode == BallMode.POSTPASS:
            self._passed_to = None
        elif self._mode in _TERMINAL_MODES:
            pass
        elif self._mode == BallMode.HELD:
            self._remove_posession()
        elif self._mode in [BallMode.MIDPASS, BallMode.MIDSHOT]:
            self._server = None
        else:
            assert False

    def _with_mode(self, mode: BallMode) -> Ball:
        self._mode = mode
        return self

    def _give_to(self, player: Player) -> Ball:
        self._position = player.position
        self._give_posession(player)
        return self._with_mode(BallMode.HELD)

    def _dead_ball(self, flip_possesion: bool) -> Ball:
        self._should_flip_posession = flip_possesion
        return self._with_mode(BallMode.DEAD)

    def held_out_of_bounds(self):
        assert self._mode == BallMode.HELD
        self._reset()
        return self._dead_ball(True)

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        assert self._mode == BallMode.HELD
        passer = self._unsafe_belongs_to()
        self._reset()
        self._server = _PassingServer(passer, receiver, self, pass_velocity)
        return self._with_mode(BallMode.MIDPASS)

    def post_pass(self, receiver: Player) -> Ball:
        assert self._mode == BallMode.MIDPASS
        self._reset()
        self._passed_to = receiver
        return self._with_mode(BallMode.POSTPASS)

    def successful_pass(self, receiver: Player) -> Ball:
        assert self._mode == BallMode.POSTPASS
        self._reset()
        return self._give_to(receiver)

    def shoot_at(self, target: Point, shot_velocity: float) -> Ball:
        assert self._mode == BallMode.HELD
        shooter = self._unsafe_belongs_to()
        self._reset()
        self._server = _ShootingServer(shooter, target, self, shot_velocity)
        return self._with_mode(BallMode.MIDSHOT)

    def post_shot(self) -> Ball:
        assert self._mode == BallMode.MIDSHOT
        self._reset()
        return self._with_mode(BallMode.POSTSHOT)

    def successful_shot(self) -> Ball:
        assert self._mode == BallMode.POSTSHOT
        self._reset()
        return self._dead_ball(True)

    def jump_ball_won_by(self, receiver: Player) -> Ball:
        assert self._mode == BallMode.DEAD
        self._reset()
        return self._give_to(receiver)
