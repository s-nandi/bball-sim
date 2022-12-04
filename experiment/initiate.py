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
    create_guaranteed_shot_probability,
)

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
    common_attributes = {"size": 0, "max_acceleration": 2.34, "max_turn_degrees": 360}
    attributes_1 = create_player_attributes(**common_attributes)
    attributes_2 = create_player_attributes(mass=2, **common_attributes)
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


def test() -> Game:
    player_size = 1.0
    width, height = 28, 15
    attributes = create_player_attributes(
        shot_probability=create_guaranteed_shot_probability(),
        max_acceleration=2.5,
        size=player_size,
    )
    player_1 = create_initialized_player(position=(4, 4), attributes=attributes)
    player_2 = create_initialized_player(position=(7, 7), attributes=attributes)
    hoop = create_hoop(width, height, 2)
    court = create_court(width, height, hoop)
    game = create_game(teams=[Team(player_1), Team(player_2)], court=court)
    game.assign_team_strategy(0, create_strategy(5))
    game.assign_team_strategy(1, create_strategy(3))
    return game
