from bball import Game
from bball.create import (
    create_initialized_player,
    create_player_attributes,
    create_linear_shot_probability,
    create_court,
    create_game,
    create_teams,
    create_game_settings,
)


def evaluation_game(num_players: int) -> Game:
    attributes = create_player_attributes(
        size=1.0,
        max_acceleration=2.34,
        max_turn_degrees=480,
        velocity_decay=0.01,
        shot_probability=create_linear_shot_probability(0.8, 0.0, 0.33, 12.1),
    )
    width = 28.65
    height = 15.24
    shot_clock = 24
    court = create_court(width, height)
    teams = []
    for _ in range(2):
        team = []
        for _ in range(num_players):
            player = create_initialized_player(attributes=attributes)
            team.append(player)
        teams.append(team)
    game = create_game(
        create_teams(*teams),
        court=court,
        settings=create_game_settings(
            shot_clock, use_expected_value_for_points=True, use_instant_inbounding=False
        ),
    )
    return game
