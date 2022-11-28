from __future__ import annotations
from enum import Enum, auto
from typing import Tuple, Optional, TYPE_CHECKING
from bball_server.utils import vector_to_string
from bball_server.passing_server import _PassingServer

if TYPE_CHECKING:
    from bball_server.player import Player


class BallMode(Enum):
    MIDPASS = auto()
    HELD = auto()
    LOOSE = auto()
    MIDSHOT = auto()


class Ball:
    _position: Tuple[float, float]
    _belongs_to: Optional[Player]
    _passing_server: Optional[_PassingServer]
    _mode: BallMode

    def __init__(self):
        self._position = (0, 0)
        self._belongs_to = None
        self._passing_server = None
        self._mode = BallMode.LOOSE

    def __repr__(self):
        return f"Ball(position = {vector_to_string(self._position)})"

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    def _unsafe_belongs_to(self) -> Player:
        assert self._belongs_to is not None
        return self._belongs_to

    def _unsafe_passing_server(self) -> _PassingServer:
        assert self._passing_server is not None
        return self._passing_server

    def give_to(self, player: Player) -> Ball:
        if self._mode == BallMode.HELD:
            self._remove_posession()
        elif self._mode == BallMode.MIDPASS:
            self._remove_posession()
            self._passing_server = None
        elif self._mode == BallMode.LOOSE:
            pass
        else:
            assert False
        self._mode = BallMode.HELD
        self._give_posession(player)
        return self

    def _give_posession(self, player: Player) -> None:
        self._belongs_to = player
        self._unsafe_belongs_to()._ball = self

    def _remove_posession(self) -> None:
        self._unsafe_belongs_to()._ball = None
        self._belongs_to = None

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        assert self._mode == BallMode.HELD
        self._mode = BallMode.MIDPASS
        self._passing_server = _PassingServer(
            self._unsafe_belongs_to(), receiver, pass_velocity
        )
        return self

    def shoot_at(self, _target: Tuple[float, float]):
        assert self._mode == BallMode.HELD
        self._mode = BallMode.MIDSHOT
        self._remove_posession()

    def _step(self, time_frame: float):
        if self._mode == BallMode.LOOSE:
            return
        if self._mode == BallMode.HELD:
            self._position = self._unsafe_belongs_to().position
            return
        if self._mode == BallMode.MIDPASS:
            self._unsafe_passing_server()._step(time_frame)
            return
        if self._mode == BallMode.MIDSHOT:
            return
        assert False, f"Invalid ball mode {self._mode}"
