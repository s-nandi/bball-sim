from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
import pymunk
from bball_server.validator import valid_pass_velocity
from bball_server.utils import convert_to_tuple

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

    def __init__(
        self, passer: Player, receiver: Player, ball: Ball, pass_velocity: float
    ):
        assert valid_pass_velocity(pass_velocity)
        assert not passer.has_ball
        assert not receiver.has_ball
        self._players_involved = PassPlayers(passer, receiver)
        self._ball = ball
        self._original_position = pymunk.Vec2d(*passer.position)
        self._pass_velocity = pass_velocity
        self._time_since_pass = 0

    def _complete_pass(self) -> bool:
        self._ball.post_pass(self._players_involved.receiver)
        return True

    def _step(self, time_step: float) -> bool:
        self._time_since_pass += time_step
        receiver_position = self._players_involved.receiver.position
        distance = self._original_position.get_distance(receiver_position)
        covered = self._pass_velocity * self._time_since_pass
        if covered >= distance:
            return self._complete_pass()
        fraction_completed = covered / distance
        assert 0.0 <= fraction_completed <= 1.0
        self._ball._position = convert_to_tuple(
            self._original_position.interpolate_to(
                receiver_position, fraction_completed
            )
        )
        return False
