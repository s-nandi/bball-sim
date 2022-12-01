from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Type, TypeVar
from bball_server.utils import coords_to_string, Point
from bball_server.ball.ball_mode import BallMode
from bball_server.ball.state import BallState
from bball_server.ball.held_ball import HeldBall
from bball_server.ball.mid_pass import MidPass
from bball_server.ball.post_pass import PostPass
from bball_server.ball.mid_shot import MidShot
from bball_server.ball.post_shot import PostShot
from bball_server.ball.dead_ball import DeadBall


if TYPE_CHECKING:
    from bball_server.player import Player

T = TypeVar("T")


def checked_type(state: BallState, state_type: Type[T]) -> T:
    assert isinstance(state, state_type)
    return state


class Ball:
    _position: Point
    _last_belonged_to: Optional[Player]
    _state: BallState

    def __init__(self):
        self._position = (0, 0)
        self._last_belonged_to = None
        self._state = DeadBall(False)

    def __repr__(self):
        return f"Ball(position = {coords_to_string(self.position)}, mode = {self.mode})"

    @property
    def position(self) -> Point:
        return self._position

    @property
    def mode(self) -> BallMode:
        return self._state.mode()

    @property
    def last_belonged_to(self) -> Optional[Player]:
        return self._last_belonged_to

    @property
    def should_flip_posession(self) -> bool:
        return checked_type(self._state, DeadBall)._should_flip_posession

    @property
    def shot_parameters(self) -> PostShot:
        return checked_type(self._state, PostShot)

    @property
    def passed_to(self) -> Player:
        return checked_type(self._state, PostPass)._receiver

    @property
    def belongs_to(self) -> Player:
        return checked_type(self._state, HeldBall)._ball_handler

    def _step(self, time_frame: float) -> bool:
        return self._state._step(time_frame)

    def _transition(self, prior_state_type: Type[BallState], state: BallState) -> Ball:
        checked_type(self._state, prior_state_type)._reset()
        self._state = state
        return self

    def held_out_of_bounds(self):
        return self._transition(HeldBall, DeadBall(True))

    def pass_to(self, receiver: Player, pass_velocity: float) -> Ball:
        return self._transition(HeldBall, MidPass(self, receiver, pass_velocity))

    def shoot_at(self, target: Point, shot_velocity: float) -> Ball:
        return self._transition(HeldBall, MidShot(self, target, shot_velocity))

    def post_pass(self, receiver: Player) -> Ball:
        return self._transition(MidPass, PostPass(receiver))

    def successful_pass(self, receiver: Player) -> Ball:
        return self._transition(PostPass, HeldBall(receiver, self))

    def post_shot(self, shooter: Player, target: Point, shot_from: Point) -> Ball:
        return self._transition(MidShot, PostShot(shooter, target, shot_from))

    def successful_shot(self) -> Ball:
        return self._transition(PostShot, DeadBall(True))

    def jump_ball_won_by(self, receiver: Player) -> Ball:
        return self._transition(DeadBall, HeldBall(receiver, self))
