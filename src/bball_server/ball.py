from __future__ import annotations
from typing import Tuple, Optional, TYPE_CHECKING
from bball_server.utils import vector_to_string
from bball_server.passing_server import _PassingServer

if TYPE_CHECKING:
    from bball_server.player import Player


class Ball:
    _position: Tuple[float, float]
    _belongs_to: Optional[Player]
    _passing_server: Optional[_PassingServer]

    def __init__(self):
        self._position = (0, 0)
        self._belongs_to = None
        self._passing_server = None

    def __repr__(self):
        return f"Ball(position = {vector_to_string(self._position)})"

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    def give_to(self, player: Player) -> Ball:
        if self._passing_server is not None:
            self._passing_server = None
        if self._belongs_to is not None:
            self._belongs_to._give_up_ball()
        player._give_ball(self)
        self._belongs_to = player
        return self

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        assert self._passing_server is None
        assert self._belongs_to is not None
        passer = self._belongs_to
        self._passing_server = _PassingServer(passer, receiver, pass_velocity)
        return self

    def _step(self, time_frame: float):
        if self._passing_server is not None:
            self._passing_server._step(time_frame)
            return
        if self._belongs_to is not None:
            self._position = self._belongs_to.position
            return
