from __future__ import annotations
from typing import Tuple
import pymunk
from bball_server.utils import convert_to_tuple, vector_to_string
from bball_server.validator import valid_multiplier
from bball_server.player.player_attributes import PlayerAttributes
from bball_server.player.player_physics import PlayerPhysics
from bball_server.player.player_move import PlayerMove


class Player:
    _attributes: PlayerAttributes
    _physics: PlayerPhysics
    _move: PlayerMove
    _has_ball: bool

    def __init__(self, attributes: PlayerAttributes):
        self._attributes = attributes
        self._physics = PlayerPhysics(attributes)
        self._move = PlayerMove()
        self._has_ball = False

    def __repr__(self) -> str:
        if not self._physics.is_initialized:
            return "UninitializedPlayer"
        position_str = "position = " + vector_to_string(self.position)
        velocity_str = "velocity = " + vector_to_string(self.velocity)
        has_ball_str = "HasBall" if self._has_ball else ""
        concat_str = ", ".join(filter(None, [position_str, velocity_str, has_ball_str]))
        return f"Player({concat_str})"

    @property
    def position(self) -> Tuple[float, float]:
        return convert_to_tuple(self._physics.position)

    @property
    def velocity(self) -> Tuple[float, float]:
        return convert_to_tuple(self._physics.velocity)

    @property
    def has_ball(self) -> bool:
        return self._has_ball

    @has_ball.setter
    def has_ball(self, value: bool) -> Player:
        assert self._has_ball != value
        self._has_ball = value
        return self

    def initial_orientation(self, orientation_degrees: float) -> Player:
        self._physics.init_orientation(orientation_degrees)
        return self

    def initial_position(self, pos_x: float, pos_y: float) -> Player:
        self._physics.init_position(pymunk.Vec2d(pos_x, pos_y))
        return self

    def turn(self, turn_degrees_multiplier: float) -> Player:
        assert valid_multiplier(turn_degrees_multiplier)
        turn_degrees = turn_degrees_multiplier * self._attributes.max_turn_degrees
        self._move.turn(turn_degrees)
        return self

    def accelerate(self, strength_multiplier: float) -> Player:
        assert valid_multiplier(strength_multiplier)
        acceleration = strength_multiplier * self._attributes.max_acceleration
        self._move.accelerate(acceleration)
        return self

    def _step(self, time_step: float) -> Player:
        self._physics.step(self._move, time_step)
        return self

    def _reset(self) -> Player:
        self._move.reset()
        return self

    def give_ball(self) -> Player:
        self.has_ball = True
        return self

    def give_up_ball(self) -> Player:
        self.has_ball = False
        return self