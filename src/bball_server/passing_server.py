from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from bball_server.player import Player


@dataclass
class PassPlayers:
    passer: Player
    receiver: Player


class PassingServer:
    _has_active_pass: bool
    _players_involved: Optional[PassPlayers]
    _steps_to_complete_pass: int

    def __init__(self):
        self._has_active_pass = False
        self._players_involved = None
        self._steps_to_complete_pass = 0

    def pass_between(
        self, passer: Player, receiver: Player, complete_in: int
    ) -> PassingServer:
        assert not self._has_active_pass
        assert complete_in > 0
        self._has_active_pass = True
        self._players_involved = PassPlayers(passer, receiver)
        self._steps_to_complete_pass = complete_in
        return self

    def _complete_pass(self):
        assert self._has_active_pass
        self._players_involved.receiver.give_ball()
        self._players_involved.passer.give_up_ball()
        self._has_active_pass = False

    def step(self) -> PassingServer:
        if self._has_active_pass:
            self._steps_to_complete_pass -= 1
            if self._steps_to_complete_pass == 0:
                self._complete_pass()
        return self
