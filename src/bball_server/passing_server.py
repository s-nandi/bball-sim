from __future__ import annotations
from dataclasses import dataclass
import pymunk
from bball_server.player import Player


@dataclass
class PassPlayers:
    passer: Player
    receiver: Player


class PassingServer:
    _has_active_pass: bool
    _players_involved: PassPlayers
    _pass_velocity: float
    _original_position: pymunk.Vec2d
    _time_since_pass: float

    def __init__(self, passer: Player, receiver: Player, pass_velocity: float):
        assert pass_velocity > 0
        assert passer.has_ball
        assert not receiver.has_ball
        self._has_active_pass = True
        self._players_involved = PassPlayers(passer, receiver)
        self._original_position = pymunk.Vec2d(*passer.position)
        self._pass_velocity = pass_velocity
        self._time_since_pass = 0

    @property
    def completed(self):
        return not self._has_active_pass

    def _complete_pass(self) -> None:
        assert self._has_active_pass
        self._players_involved.receiver._give_ball()
        self._players_involved.passer._give_up_ball()
        self._has_active_pass = False

    def _step(self, time_step: float) -> PassingServer:
        assert self._has_active_pass
        self._time_since_pass += time_step
        receiver_position = self._players_involved.receiver.position
        distance = self._original_position.get_distance(receiver_position)
        covered = self._pass_velocity * self._time_since_pass
        if covered >= distance:
            self._complete_pass()
        return self
