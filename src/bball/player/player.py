from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from bball.utils import coords_to_string, ROUND_DIGITS, angle_degrees_to_vector
from bball.validator import valid_multiplier, valid_angle_degrees
from bball.player.player_attributes import PlayerAttributes
from bball.player.player_physics import PlayerPhysics
from bball.player.player_move import PlayerMove

if TYPE_CHECKING:
    from bball.ball import Ball
    from bball.utils import Point, Vector


class Player:
    _attributes: PlayerAttributes
    _physics: PlayerPhysics
    _move: PlayerMove
    _ball: Optional[Ball]

    def __init__(self, attributes: PlayerAttributes):
        self._attributes = attributes
        self._physics = PlayerPhysics(attributes.physical)
        self._move = PlayerMove()
        self._ball = None

    def __repr__(self) -> str:
        if not self.is_initialized:
            return "UninitializedPlayer"
        position_str = f"position={coords_to_string(self.position)}"
        velocity_str = f"velocity={coords_to_string(self.velocity)}"
        orientation_str = f"orientation={round(self.orientation_degrees, ROUND_DIGITS)}"
        has_ball_str = "HasBall" if self.has_ball else ""
        concat_str = ",".join(
            filter(None, [position_str, velocity_str, orientation_str, has_ball_str])
        )
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
    def acceleration(self) -> Vector:
        assert self.is_initialized
        return self._physics.acceleration

    @property
    def physical_attributes(self) -> PlayerAttributes.Physical:
        return self._attributes.physical

    @property
    def skill_attributes(self) -> PlayerAttributes.Skill:
        return self._attributes.skill

    @property
    def orientation_degrees(self) -> float:
        assert self.is_initialized
        orientation_degrees = self._physics.orientation_degrees
        assert valid_angle_degrees(orientation_degrees)
        return orientation_degrees

    @property
    def has_ball(self) -> bool:
        assert self.is_initialized
        return self._ball is not None

    @property
    def is_initialized(self):
        return self._physics.is_initialized

    @property
    def ball(self) -> Ball:
        assert self.is_initialized
        assert self._ball is not None
        return self._ball

    def place_at(self, position: Point, orientation_degrees: float) -> Player:
        self._physics.reset_velocity()
        self._physics.position = position
        self._physics.orientation_degrees = orientation_degrees
        return self

    def with_velocity(self, velocity_magnitude: float) -> Player:
        self._physics.velocity = angle_degrees_to_vector(
            self.orientation_degrees, velocity_magnitude
        )
        return self

    def turn(self, multiplier: float) -> Player:
        assert self.is_initialized
        assert valid_multiplier(multiplier)
        turn_degrees = multiplier * self._attributes.physical.max_turn_degrees
        self._move.turn(turn_degrees)
        return self

    def accelerate(self, multiplier: float) -> Player:
        assert self.is_initialized
        # TODO: Require multiplier in [-0.5, 1] range to prevent rapid backpedaling
        assert valid_multiplier(multiplier)
        acceleration = multiplier * self._attributes.physical.max_acceleration
        self._move.accelerate(acceleration)
        return self

    def pass_to(self, receiver: Player) -> Player:
        assert self.is_initialized
        self._move.pass_to(self.ball, receiver, self.skill_attributes.pass_velocity)
        return self

    def shoot_at(self, target: Point) -> Player:
        assert self.is_initialized
        self._move.shoot_at(self.ball, target, self.skill_attributes.shot_velocity)
        return self

    def _step(self, time_step: float) -> bool:
        assert self.is_initialized
        self._move.do_action()
        return self._physics._step(self._move, time_step)

    def _reset(self) -> Player:
        assert self.is_initialized
        self._move.reset()
        return self
