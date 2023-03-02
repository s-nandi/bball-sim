from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from bball.utils import approx

if TYPE_CHECKING:
    from bball.player import Player


class BehaviorInterface(ABC):
    _time_frame: float
    _has_run: bool = False

    def drive(self, player: Player, time_frame: float) -> bool:
        if not self._has_run:
            self._has_run = True
            self._time_frame = time_frame
        assert approx(self._time_frame, time_frame)
        return self._drive(player)

    @abstractmethod
    def _drive(self, player: Player) -> bool:
        pass
