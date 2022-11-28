from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import pymunk

if TYPE_CHECKING:
    from bball_server.player import Player
    from bball_server.ball import Ball


class _ShootingServer:
    _shooter: Player
    _ball: Ball
    _target: Tuple[float, float]
    _shot_velocity: float
    _original_position: pymunk.Vec2d
    _time_since_shot: float

    def __init__(
        self, shooter: Player, target: Tuple[float, float], shot_velocity: float
    ):
        assert shot_velocity > 0
        assert shooter.has_ball
        self._shooter = shooter
        self._ball = shooter._unsafe_ball()
        self._target = target
        self._shot_velocity = shot_velocity
        self._original_position = pymunk.Vec2d(*shooter.position)
        self._time_since_shot = 0.0
        self._ball._remove_posession()

    def _complete_shot(self) -> None:
        self._ball._position = self._target
        self._ball.post_shot()

    def _step(self, time_step: float) -> _ShootingServer:
        self._time_since_shot += time_step
        covered = self._time_since_shot * self._shot_velocity
        distance = self._original_position.get_distance(self._target)
        if covered >= distance:
            self._complete_shot()
        else:
            fraction_completed = covered / distance
            assert 0.0 <= fraction_completed <= 1.0
            position = self._original_position.interpolate_to(
                self._target, fraction_completed
            )
            self._ball._position = position
        return self
