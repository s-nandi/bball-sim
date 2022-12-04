from bball import Game
from bball.create import (
    create_teams,
    create_game,
    create_game_settings,
    create_initialized_player,
    create_court,
    create_player_attributes,
    copy_player_attributes,
    create_hoop,
    create_three_point_line,
    create_strategy,
)

USE_EXPECTED_VALUE = True


def multiple_players(num_players_per_team: int) -> Game:
    size = 1.0
    attributes = create_player_attributes(
        size=1.0, max_acceleration=2.34, max_turn_degrees=360, velocity_decay=0.01
    )
    attributes_list = copy_player_attributes(attributes, num_players_per_team)
    width = 28.65
    height = 15.24

    teams = [[], []]
    for player_index, attributes in enumerate(attributes_list):
        offset = 2 * (player_index + 1) * size
        player_1 = create_initialized_player(
            position=(4, height / 2 + offset), attributes=attributes
        )
        player_2 = create_initialized_player(
            position=(4, height / 2 - offset), attributes=attributes
        )
        teams[0].append(player_1)
        teams[1].append(player_2)

    hoop = create_hoop(width, height, 1.6, create_three_point_line(width, height))
    game = (
        create_game(
            teams=create_teams(teams[0], teams[1]),
            court=create_court(width, height, hoop),
            settings=create_game_settings(
                use_expected_value_for_points=USE_EXPECTED_VALUE,
                use_instant_inbounding=False,
                shot_clock_duration=24.0,
            ),
        )
        .assign_team_strategy(0, create_strategy(2))
        .assign_team_strategy(1, create_strategy(10))
    )
    return game
