from __future__ import annotations
import pymunk
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
        self._physics = PlayerPhysics(attributes.velocity_decay)
        self._move = PlayerMove()
        self._has_ball = False

    def __repr__(self):
        if not self._physics.is_initialized:
            return "UninitializedPlayer"
        position_x = round(self.position[0])
        position_y = round(self.position[1])
        position_str = f"({position_x}, {position_y})"
        return f"Player(position = {position_str})"

    def initial_orientation(self, orientation_degrees: float):
        self._physics.init_orientation(orientation_degrees)
        return self

    def initial_position(self, pos_x: float, pos_y: float):
        self._physics.init_position(pymunk.Vec2d(pos_x, pos_y))
        return self

    def turn(self, turn_degrees_multiplier: float):
        assert self._physics.is_initialized
        assert valid_multiplier(turn_degrees_multiplier)
        turn_degrees = turn_degrees_multiplier * self._attributes.max_turn_degrees
        self._move.turn(turn_degrees)
        return self

    def accelerate(self, strength_multiplier: float):
        assert self._physics.is_initialized
        assert valid_multiplier(strength_multiplier)
        acceleration = strength_multiplier * self._attributes.max_acceleration
        self._move.accelerate(acceleration)
        return self

    @property
    def position(self):
        return tuple(self._physics.position)

    @property
    def velocity(self):
        return tuple(self._physics.velocity)

    def step(self):
        self._physics.step(self._move)
        self._move = PlayerMove()
        return self

    def _set_has_ball(self, has_ball_state: bool) -> Player:
        assert self._has_ball != has_ball_state
        self._has_ball = has_ball_state
        return self

    @property
    def has_ball(self):
        return self._has_ball

    def give_ball(self):
        self._set_has_ball(True)
        return True

    def pass_to(self, other: Player):
        self._set_has_ball(False)
        other._set_has_ball(True)
        return self
