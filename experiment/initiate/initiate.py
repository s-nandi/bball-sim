from bball import Game
from bball.create import (
    create_teams,
    create_game,
    create_game_settings,
    create_initialized_player,
    create_court,
    create_player_attributes,
    create_hoop,
    create_three_point_line,
    create_strategy,
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
    hoop = create_hoop(width, height, 1.6, create_three_point_line(width, height))
    game = (
        create_game(
            teams=create_teams(player_1, player_2),
            court=create_court(width, height, hoop),
            settings=create_game_settings(
                use_expected_value_for_points=USE_EXPECTED_VALUE
            ),
        )
        .assign_team_strategy(0, create_strategy(0.1))
        .assign_team_strategy(1, create_strategy(10))
    )
    return game
