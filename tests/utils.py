from typing import Tuple, TypeVar, Callable, Any
from bball_server import Player, PlayerAttributes

T = TypeVar("T")


def create_uninitialized_player(
    max_acceleration: float = 1.0,
    max_turn_degrees: float = 90.0,
    velocity_decay: float = 0.0,
) -> Player:
    return Player(
        PlayerAttributes(
            max_acceleration=max_acceleration,
            max_turn_degrees=max_turn_degrees,
            velocity_decay=velocity_decay,
        )
    )


def create_initialized_player(
    max_acceleration: float = 1.0,
    max_turn_degrees: float = 90.0,
    velocity_decay: float = 0.0,
) -> Player:
    player = Player(
        PlayerAttributes(
            max_acceleration=max_acceleration,
            max_turn_degrees=max_turn_degrees,
            velocity_decay=velocity_decay,
        )
    )
    player.initial_position(0, 0).initial_orientation(0)
    return player


def close_to(
    vec_1: Tuple[float, float], vec_2: Tuple[float, float], eps: float = 10**-6
) -> bool:
    delta_y = vec_1[0] - vec_2[0]
    delta_y = vec_1[1] - vec_2[1]
    return abs(delta_y) < eps and abs(delta_y) < eps


def require_exception(callback: Callable[[], T], exception_type: Any):
    success = False
    try:
        callback()
    except exception_type:
        success = True
    assert success
