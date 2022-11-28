from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from bball_server.utils import coords_to_string
from bball_server.validator import valid_multiplier
from bball_server.player.player_attributes import PlayerAttributes
from bball_server.player.player_physics import PlayerPhysics
from bball_server.player.player_move import PlayerMove

if TYPE_CHECKING:
    from bball_server.ball import Ball
    from bball_server.utils import Point, Vector


class Player:
    _attributes: PlayerAttributes
    _physics: PlayerPhysics
    _move: PlayerMove
    _ball: Optional[Ball]

    def __init__(self, attributes: PlayerAttributes):
        self._attributes = attributes
        self._physics = PlayerPhysics(attributes)
        self._move = PlayerMove()
        self._ball = None

    def __repr__(self) -> str:
        if not self.is_initialized:
            return "UninitializedPlayer"
        position_str = "position = " + coords_to_string(self.position)
        velocity_str = "velocity = " + coords_to_string(self.velocity)
        has_ball_str = "HasBall" if self.has_ball else ""
        concat_str = ", ".join(filter(None, [position_str, velocity_str, has_ball_str]))
        return f"Player({concat_str})"

    @property
    def position(self) -> Point:
        assert self.is_initialized
        return self._physics.position

    @property
    def velocity(self) -> Vector:
        assert self.is_initialized
        return self._physics.velocity

    @property
    def has_ball(self) -> bool:
        assert self.is_initialized
        return self._ball is not None

    @property
    def is_initialized(self):
        return self._physics.is_initialized

    def _unsafe_ball(self) -> Ball:
        assert self.is_initialized
        assert self._ball is not None
        return self._ball

    def place_at(self, position: Point, orientation_degrees: float) -> Player:
        self._physics.position = position
        self._physics.orientation = orientation_degrees
        return self

    def turn(self, turn_degrees_multiplier: float) -> Player:
        assert self.is_initialized
        assert valid_multiplier(turn_degrees_multiplier)
        turn_degrees = turn_degrees_multiplier * self._attributes.max_turn_degrees
        self._move.turn(turn_degrees)
        return self

    def accelerate(self, strength_multiplier: float) -> Player:
        assert self.is_initialized
        assert valid_multiplier(strength_multiplier)
        acceleration = strength_multiplier * self._attributes.max_acceleration
        self._move.accelerate(acceleration)
        return self

    def pass_to(self, receiver: Player, pass_velocity: float) -> Player:
        assert self.is_initialized
        self._unsafe_ball().pass_to(receiver, pass_velocity)
        return self

    def shoot_at(self, target: Point, shot_velocity: float) -> Player:
        assert self.is_initialized
        self._unsafe_ball().shoot_at(target, shot_velocity)
        return self

    def _step(self, time_step: float) -> bool:
        assert self.is_initialized
        return self._physics._step(self._move, time_step)

    def _reset(self) -> Player:
        assert self.is_initialized
        self._move.reset()
        return self
