from bball import Game, Team
from bball.create import (
    create_game,
    create_game_settings,
    create_initialized_player,
    create_court,
    create_player_attributes,
    create_hoop,
    create_three_point_line,
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
    return create_game(
        teams=[Team(player_1), Team(player_2)],
        court=court,
        settings=create_game_settings(USE_EXPECTED_VALUE),
    )
