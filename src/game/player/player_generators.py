import itertools
from typing import Union, Iterable, List, Tuple, TypeVar
from game.player.player import Player
from game.player.player_attributes import PlayerAttributes
from game.team import Team

T = TypeVar("T")


def assert_generated_list_length(generated_list: List[T], expected_length: int):
    if len(generated_list) < expected_length:
        error_message = (
            f"Generators provided {len(generated_list)} values"
            f"while {expected_length} were required"
        )
        assert False, error_message


def generate_player_attributes(
    *,
    mass_generator: Iterable[float],
    size_generator: Iterable[float],
    max_speed_generator: Iterable[float],
    max_acceleration_generator: Iterable[float],
    num_attributes: Union[int, None] = None,
) -> Iterable[PlayerAttributes]:
    attributes: Iterable[PlayerAttributes] = (
        PlayerAttributes(
            mass=mass,
            size=size,
            max_speed=max_speed,
            max_acceleration=max_acceleration,
        )
        for mass, size, max_speed, max_acceleration in itertools.islice(
            zip(
                mass_generator,
                size_generator,
                max_speed_generator,
                max_acceleration_generator,
            ),
            num_attributes,
        )
    )
    if num_attributes is not None:
        attributes = list(attributes)
        assert_generated_list_length(attributes, num_attributes)

    return attributes


def generate_players(
    *,
    mass_generator: Iterable[float],
    size_generator: Iterable[float],
    max_speed_generator: Iterable[float],
    max_acceleration_generator: Iterable[float],
    position_generator: Iterable[Tuple[float, float]],
    teams_generator: Iterable[Team],
    num_players: Union[int, None] = None,
) -> Iterable[Player]:
    attributes = generate_player_attributes(
        mass_generator=mass_generator,
        size_generator=size_generator,
        max_speed_generator=max_speed_generator,
        max_acceleration_generator=max_acceleration_generator,
        num_attributes=num_players,
    )
    players: Iterable[Player] = (
        Player(attribute, position, team)
        for attribute, position, team in zip(
            attributes, position_generator, teams_generator
        )
    )
    if num_players is not None:
        players = list(players)
        assert_generated_list_length(players, num_players)
    return players
