from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import pymunk
from bball_server.player import Player
from bball_server.utils import convert_to_tuple


@dataclass
class PassPlayers:
    passer: Player
    receiver: Player


class PassingServer:
    _has_active_pass: bool
    _players_involved: Optional[PassPlayers]
    _pass_velocity: float
    _original_position: pymunk.Vec2d
    _time_since_pass: float

    def __init__(self):
        self._reset()

    def pass_between(
        self, passer: Player, receiver: Player, pass_velocity: float
    ) -> PassingServer:
        assert not self._has_active_pass
        assert pass_velocity > 0
        self._has_active_pass = True
        self._players_involved = PassPlayers(passer, receiver)
        self._pass_velocity = pass_velocity
        self._original_position = pymunk.Vec2d(*passer.position)
        return self

    def _complete_pass(self) -> None:
        assert self._has_active_pass
        self._players_involved.receiver.give_ball()
        self._players_involved.passer.give_up_ball()
        self._reset()

    def _reset(self) -> None:
        self._has_active_pass = False
        self._players_involved = None
        self._original_position = pymunk.Vec2d(0, 0)
        self._pass_velocity = 0
        self._has_active_pass = False
        self._time_since_pass = 0

    def _step(self, time_step: float) -> PassingServer:
        if not self._has_active_pass:
            return self
        self._time_since_pass += time_step
        receiver_position = self._players_involved.receiver.position
        distance = self._original_position.get_distance(receiver_position)
        covered = self._pass_velocity * self._time_since_pass
        if covered >= distance:
            self._complete_pass()
        return self
