from typing import Tuple, TypeVar, Callable, Any, Optional
from bball_server import (
    Player,
    PlayerAttributes,
    Space,
    Ball,
    Court,
    Hoop,
    ThreePointLine,
    RectangleThreePointLine,
    LinearShotProbability,
    Game,
)

T = TypeVar("T")


def create_space() -> Space:
    return Space()


def create_ball() -> Ball:
    return Ball()


DEFAULT_WIDTH_RATIO = 1 / 4
DEFAULT_HEIGHT_RATIO = 1 / 5


def create_three_point_line(
    width: float,
    height: float,
    width_ratio: float = DEFAULT_WIDTH_RATIO,
    height_ratio: float = DEFAULT_HEIGHT_RATIO,
) -> RectangleThreePointLine:
    """
    Returns a rectangular three point line for the left side of the court
    that spans from 0 to width * width_ratio along the x-axis, and from
    height_ratio * height to (1 - height_ratio) * height along the y-axis
    """
    assert width_ratio < 0.5, "Entire width of court is in 3-point range"
    assert height_ratio < 0.5, "Entire height of court is in 3-point range"
    distance_from_left = width * width_ratio
    distance_from_bottom = height * height_ratio
    line = RectangleThreePointLine(
        0, distance_from_left, distance_from_bottom, height - distance_from_bottom
    )
    return line


def create_hoop(
    width: float,
    height: float,
    three_point_line: Optional[ThreePointLine] = None,
):
    if three_point_line is None:
        three_point_line = create_three_point_line(width, height)
    return Hoop(1, height / 2, three_point_line)


def create_court(
    width: float = 12,
    height: float = 5,
    hoop: Optional[Hoop] = None,
) -> Court:
    if hoop is None:
        hoop = create_hoop(width, height)
    return Court(dimensions=(width, height), hoops=(hoop, hoop.other_hoop(width)))


def create_shot_probability(
    max_percentage: float = 1.0,
    min_shot_distance: float = 0.0,
    min_percentage: float = 0.0,
    max_shot_distance: float = 100.0,
) -> LinearShotProbability:
    return LinearShotProbability(
        max_percentage, min_shot_distance, min_percentage, max_shot_distance
    )


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
    return player.place_at(position, orientation_degrees)


def create_game(teams):
    return Game(teams, create_ball(), create_court())


DEFAULT_EPS = 10**-6


def approx(value_1: float, value_2: float, eps: float = DEFAULT_EPS):
    return abs(value_1 - value_2) < eps


def close_to(
    vec_1: Tuple[float, float], vec_2: Tuple[float, float], eps: float = DEFAULT_EPS
) -> bool:
    delta_x = vec_1[0] - vec_2[0]
    delta_y = vec_1[1] - vec_2[1]
    return approx(delta_x, 0, eps) and approx(delta_y, 0, eps)


def require_exception(callback: Callable[[], T], exception_type: Any):
    success = False
    try:
        callback()
    except exception_type:
        success = True
    assert success
