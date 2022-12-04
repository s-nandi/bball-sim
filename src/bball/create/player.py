from typing import Tuple
from bball.player import Player, PlayerAttributes
from bball.shot_probability import ShotProbability
from bball.create.shot_probability import DEFAULT_SHOT_PROBABILITY

# pylint: disable=too-many-arguments
def create_player_attributes(
    *,
    mass: float = 1.0,
    size: float = 0,
    max_acceleration: float = 1.0,
    max_turn_degrees: float = 90.0,
    velocity_decay: float = 0.0,
    shot_probability: ShotProbability = DEFAULT_SHOT_PROBABILITY,
    shot_velocity: float = 10.0,
    pass_velocity: float = 6.0,
) -> PlayerAttributes:
    return PlayerAttributes(
        PlayerAttributes.Physical(
            mass=mass,
            size=size,
            max_acceleration=max_acceleration,
            max_turn_degrees=max_turn_degrees,
            velocity_decay=velocity_decay,
        ),
        PlayerAttributes.Skill(
            shot_probability=shot_probability,
            shot_velocity=shot_velocity,
            pass_velocity=pass_velocity,
        ),
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
