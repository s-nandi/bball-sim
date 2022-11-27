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

    def give_to(self, player: Player) -> Ball:
        if self._mode == BallMode.HELD:
            self._belongs_to._give_up_ball()
        elif self._mode == BallMode.MIDPASS:
            self._belongs_to._give_up_ball()
            self._passing_server = None
        elif self._mode == BallMode.LOOSE:
            pass
        else:
            assert False
        self._mode = BallMode.HELD
        player._give_ball(self)
        return self

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        assert self._mode == BallMode.HELD
        self._mode = BallMode.MIDPASS
        passer = self._belongs_to
        self._passing_server = _PassingServer(passer, receiver, pass_velocity)
        return self

    def _step(self, time_frame: float):
        if self._mode == BallMode.LOOSE:
            return
        if self._mode == BallMode.HELD:
            self._position = self._belongs_to.position
            return
        if self._mode == BallMode.MIDPASS:
            self._passing_server._step(time_frame)
            return
        assert False, f"Invalid ball mode {self._mode}"
