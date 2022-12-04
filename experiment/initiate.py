from bball import Game, Team
from bball.create import (
    create_game,
    create_game_settings,
    create_initialized_player,
    create_court,
    create_player_attributes,
    create_hoop,
    create_three_point_line,
    create_strategy,
)
from tests import test_strategy as tests  # pylint: disable=unused-import

USE_EXPECTED_VALUE = True


def two_uniform_players() -> Game:
    attributes = create_player_attributes(max_acceleration=2.34, max_turn_degrees=360)
    width = 28.65
    height = 15.24
    player_1 = create_initialized_player(
        position=(4, height / 2 + 2), attributes=attributes
    )
    player_2 = create_initialized_player(
        position=(4, height / 2 - 2), attributes=attributes
    )
    three_point_line = create_three_point_line(width, height)
    hoop = create_hoop(width, height, 1.6, three_point_line)
    court = create_court(width, height, hoop)
    game = create_game(
        teams=[Team(player_1), Team(player_2)],
        court=court,
        settings=create_game_settings(USE_EXPECTED_VALUE),
    )
    game.assign_team_strategy(0, create_strategy(0.1))
    game.assign_team_strategy(1, create_strategy(10))
    return game


def players_collision() -> Game:
    # TODO: Change size once behaviors are robust to collisions
    size = 0
    max_acceleration = 2.34
    max_turn_degrees = 360
    attributes_1 = create_player_attributes(
        size=size, max_acceleration=max_acceleration, max_turn_degrees=max_turn_degrees
    )
    attributes_2 = create_player_attributes(
        mass=2,
        size=size,
        max_acceleration=max_acceleration,
        max_turn_degrees=max_turn_degrees,
    )
    width = 28.65
    height = 15.24
    player_1 = create_initialized_player(
        position=(4, height / 2), attributes=attributes_1
    )
    player_2 = create_initialized_player(
        position=(8, height / 2), attributes=attributes_2
    )
    three_point_line = create_three_point_line(width, height)
    hoop = create_hoop(width, height, 1.6, three_point_line)
    court = create_court(width, height, hoop)
    game = create_game(
        teams=[Team(player_1), Team(player_2)],
        court=court,
        settings=create_game_settings(USE_EXPECTED_VALUE),
    )
    game.assign_team_strategy(0, create_strategy(0.1))
    game.assign_team_strategy(1, create_strategy(20))
    return game
