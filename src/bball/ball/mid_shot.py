from __future__ import annotations
from typing import TYPE_CHECKING
import pymunk
from bball.validator import valid_shot_velocity
from bball.utils import convert_to_tuple, approx
from bball.ball.state import BallState
from bball.ball.ball_mode import BallMode

if TYPE_CHECKING:
    from bball.player import Player
    from bball.ball import Ball
    from bball.utils import Point


class MidShot(BallState):
    _shooter: Player
    _ball: Ball
    _target: Point
    _shot_velocity: float
    _original_position: pymunk.Vec2d
    _time_since_shot: float

    def __init__(self, ball: Ball, target: Point, shot_velocity: float):
        assert valid_shot_velocity(shot_velocity)
        shooter = ball.belongs_to
        self._shooter = shooter
        self._ball = ball
        self._target = target
        self._shot_velocity = shot_velocity
        self._original_position = pymunk.Vec2d(*shooter.position)
        self._time_since_shot = 0.0

    def _complete_shot(self) -> bool:
        self._ball._position = self._target
        self._ball.post_shot(self._shooter, self._target, self._original_position)
        return True

    def _step(self, time_step: float) -> bool:
        self._time_since_shot += time_step
        covered = self._time_since_shot * self._shot_velocity
        distance = self._original_position.get_distance(self._target)
        if approx(covered, distance) or covered > distance:
            return self._complete_shot()
        fraction_completed = covered / distance
        assert 0.0 <= fraction_completed <= 1.0
        position = convert_to_tuple(
            self._original_position.interpolate_to(self._target, fraction_completed)
        )
        self._ball._position = position
        return False

    @staticmethod
    def mode() -> BallMode:
        return BallMode.MIDSHOT
