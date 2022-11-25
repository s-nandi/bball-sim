from typing import Tuple, TypeVar, Callable, Any
from bball_server import Player, PlayerAttributes, Space

T = TypeVar("T")


def create_space() -> Space:
    return Space()


def create_player_attributes(
    mass: float = 1.0,
    max_acceleration: float = 1.0,
    max_turn_degrees: float = 90.0,
    velocity_decay: float = 0.0,
) -> PlayerAttributes:
    return PlayerAttributes(
        mass=mass,
        max_acceleration=max_acceleration,
        max_turn_degrees=max_turn_degrees,
        velocity_decay=velocity_decay,
    )


DEFAULT_PLAYER_ATTRIBUTES = create_player_attributes()


def create_uninitialized_player(
    attributes: PlayerAttributes = DEFAULT_PLAYER_ATTRIBUTES,
) -> Player:
    return Player(attributes)


def create_initialized_player(
    attributes: PlayerAttributes = DEFAULT_PLAYER_ATTRIBUTES,
    position: Tuple[float, float] = (0.0, 0.0),
    orientation_degrees: float = 0.0,
) -> Player:
    player = Player(attributes)
    return player.initial_position(*position).initial_orientation(orientation_degrees)


def close_to(
    vec_1: Tuple[float, float], vec_2: Tuple[float, float], eps: float = 10**-6
) -> bool:
    delta_x = vec_1[0] - vec_2[0]
    delta_y = vec_1[1] - vec_2[1]
    return abs(delta_x) < eps and abs(delta_y) < eps


def require_exception(callback: Callable[[], T], exception_type: Any):
    success = False
    try:
        callback()
    except exception_type:
        success = True
    assert success
