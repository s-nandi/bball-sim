from __future__ import annotations
from typing import Tuple, Optional, TYPE_CHECKING
from bball_server.utils import vector_to_string

if TYPE_CHECKING:
    from bball_server.player import Player


class Ball:
    _position: Tuple[float, float]
    _belongs_to: Optional[Player]

    def __init__(self):
        self._position = (0, 0)
        self._belongs_to = None

    def __repr__(self):
        return f"Ball(position = {vector_to_string(self._position)})"

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    def give_to(self, player: Player) -> Ball:
        if self._belongs_to is not None:
            self._belongs_to._give_up_ball()
        player._give_ball(self)
        self._position = player.position
        self._belongs_to = player
        return self

    def _step(self, _time_frame: float):
        if self._belongs_to is not None:
            self._position = self._belongs_to.position
