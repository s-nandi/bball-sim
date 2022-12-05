from typing import List
from bball import Game, Player
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
    created_spaced_strategy,
    create_linear_shot_probability,
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

    teams: List[List[Player]] = [[], []]
    for player_index, attributes in enumerate(attributes_list, start=1):
        attributes_1, attributes_2 = copy_player_attributes(attributes, 2)

        attributes_1.physical.size += 0.2 * player_index
        attributes_2.physical.size += 0.4
        attributes_1.physical.mass += player_index
        attributes_2.physical.mass += 5
        attributes_1.physical.max_acceleration -= 0.5 * player_index
        attributes_2.physical.max_acceleration -= 0.8
        attributes_1.skill.shot_probability = create_linear_shot_probability(
            0.8, 0, 0.1 * player_index, width / 2
        )
        attributes_2.skill.shot_probability = create_linear_shot_probability(
            0.8, 0, 0.3 * player_index, 4.0
        )

        offset = 2 * (player_index + 1) * size
        player_1 = create_initialized_player(
            position=(4, height / 2 + offset), attributes=attributes_1
        )
        player_2 = create_initialized_player(
            position=(4, height / 2 - offset), attributes=attributes_2
        )
        teams[0].append(player_1)
        teams[1].append(player_2)

    hoop = create_hoop(width, height, 1.6, create_three_point_line(width, height))
    strategy_1 = created_spaced_strategy(
        spacing_distance=6.5, pass_probability=0.03, shot_quality_threshold=2.0
    )
    strategy_2 = created_spaced_strategy(
        spacing_distance=3,
        pass_probability=1.0,
        shot_quality_threshold=2.5,
        dive_to_basket=True,
    )
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
        .assign_team_strategy(0, strategy_1)
        .assign_team_strategy(1, strategy_2)
    )
    return game
