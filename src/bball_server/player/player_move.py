from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from bball_server.player import Player
    from bball_server.ball import Ball
    from bball_server.utils import Point


@dataclass
class PlayerPass:
    ball: Ball
    receiver: Player
    velocity: float
    _executed: bool = field(init=False, default=False)

    def name(self):
        return "pass"

    def execute(self):
        assert not self._executed
        self._executed = True
        self.ball.pass_to(self.receiver, self.velocity)


@dataclass
class PlayerShot:
    ball: Ball
    target: Point
    velocity: float
    _executed: bool = field(init=False, default=False)

    @property
    def name(self):
        return "shoot"

    def execute(self):
        assert not self._executed
        self._executed = True
        self.ball.shoot_at(self.target, self.velocity)


PlayerAction = Union[PlayerPass, PlayerShot]


class PlayerMove:
    _acceleration: Optional[float] = None
    _turn_degrees: Optional[float] = None
    _action: Optional[PlayerAction] = None

    def _assert_pre_acceleration(self, move_name: str):
        error_msg = f"Cannot {move_name} after accelerating in the same step"
        assert self._acceleration is None, error_msg

    def _assert_pre_action(self, move_name: str):
        if self._action is not None:
            action_name = self._action.name
            error_msg = f"Cannot {move_name} after {action_name}ing in the same step"
            assert self._action is None, error_msg

    def turn(self, turn_degrees: float):
        assert self._turn_degrees is None
        self._assert_pre_acceleration("turn")
        self._turn_degrees = turn_degrees

    def accelerate(self, acceleration: float):
        assert self._acceleration is None
        self._assert_pre_action("accelerate")
        self._acceleration = acceleration

    def pass_to(self, ball: Ball, receiver: Player, velocity: float):
        assert self._action is None
        self._action = PlayerPass(ball, receiver, velocity)

    def shoot_at(self, ball: Ball, target: Point, velocity: float):
        assert self._action is None
        self._action = PlayerShot(ball, target, velocity)

    def reset(self):
        if self._action is not None:
            self._action.execute()
        self._acceleration = None
        self._turn_degrees = None
        self._action = None

    @property
    def acceleration(self) -> float:
        if self._acceleration is None:
            return 0.0
        return self._acceleration

    @property
    def turn_degrees(self) -> float:
        if self._turn_degrees is None:
            return 0.0
        return self._turn_degrees
