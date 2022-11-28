from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
import pymunk

if TYPE_CHECKING:
    from bball_server.player import Player
    from bball_server.ball import Ball


@dataclass
class PassPlayers:
    passer: Player
    receiver: Player


class _PassingServer:
    _players_involved: PassPlayers
    _ball: Ball
    _pass_velocity: float
    _original_position: pymunk.Vec2d
    _time_since_pass: float

    def __init__(self, passer: Player, receiver: Player, pass_velocity: float):
        assert pass_velocity > 0
        assert passer.has_ball
        assert not receiver.has_ball
        self._players_involved = PassPlayers(passer, receiver)
        self._ball = passer._unsafe_ball()
        self._original_position = pymunk.Vec2d(*passer.position)
        self._pass_velocity = pass_velocity
        self._time_since_pass = 0
        self._ball._remove_posession()

    def _complete_pass(self) -> None:
        self._ball.post_pass()

    def _step(self, time_step: float) -> _PassingServer:
        self._time_since_pass += time_step
        receiver_position = self._players_involved.receiver.position
        distance = self._original_position.get_distance(receiver_position)
        covered = self._pass_velocity * self._time_since_pass
        if covered >= distance:
            self._complete_pass()
        else:
            fraction_completed = covered / distance
            assert 0.0 <= fraction_completed <= 1.0
            self._ball._position = self._original_position.interpolate_to(
                receiver_position, fraction_completed
            )
        return self
