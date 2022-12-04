import math
from typing import Tuple
import pytest
from bball import BallMode, Game, Court, Player
from bball.behavior import ReachVelocity
from bball.strategy import RunToBasketAndShoot, StandBetweenBasket, UseBehavior
from bball.utils import distance_between, close_to, vector_length, approx
from bball.create import (
    create_initialized_player,
    create_teams,
    create_space,
    create_game,
    create_court,
    create_guaranteed_shot_probability,
    create_player_attributes,
    create_strategy,
    create_hoop,
    create_three_point_line,
    create_game_settings,
)


def assert_relatively_on_court(court: Court, player: Player, threshold: float):
    position_x = player.position[0]
    position_y = player.position[1]
    assert position_x >= -threshold
    assert position_x <= court.width + threshold
    assert position_y >= -threshold
    assert position_y <= court.height + threshold


def test_run_to_basket_strategy():
    player = create_initialized_player()
    game = create_game(teams=create_teams(player))
    space = create_space().add(player)
    ball = game.ball
    ball.jump_ball_won_by(player)

    time_frame = 1
    steps = 20
    threshold = 5
    strategy = RunToBasketAndShoot(threshold).for_team_index_in_game(0, game)
    target_hoop = game.target_hoop(player)
    did_shoot = False
    for _ in range(steps):
        is_close_enough = (
            distance_between(player.position, target_hoop.position) <= threshold
        )
        strategy.drive(time_frame)
        space.step(time_frame)
        if ball.mode in [BallMode.MIDSHOT, BallMode.REACHEDSHOT]:
            did_shoot = True
        if is_close_enough:
            assert did_shoot
    assert did_shoot


@pytest.mark.parametrize("attacker_accel", [0.1, 0.5, 0.8, 0.9, 1.0])
def test_stand_between_player_and_basket(attacker_accel):
    width = 20
    height = 10
    initial_padding = 3
    player_1 = create_initialized_player(position=(0, height / 2))
    player_2 = create_initialized_player(position=(initial_padding, height / 2))
    court = create_court(width, height)
    game = create_game(teams=create_teams(player_1, player_2), court=court)
    space = create_space().add(game)
    ball = game.ball
    ball.jump_ball_won_by(player_1)
    player_1.accelerate(attacker_accel)
    time_frame = 0.1
    strategy = StandBetweenBasket().for_team_index_in_game(1, game)
    target_hoop = game.target_hoop(player_1)
    for _ in range(width - initial_padding - 1):
        assert player_1.position[0] <= target_hoop.position[0]
        assert player_1.position[0] <= player_2.position[0] <= target_hoop.position[0]
        strategy.drive(time_frame)
        space.step(time_frame)


def test_use_behavior():
    time_frame = 0.2
    player = create_initialized_player()
    target_velocity = (5.0, 5.0)
    max_turn_degrees = player.physical_attributes.max_turn_degrees
    orientation_steps = math.ceil(360 / max_turn_degrees / time_frame)
    velocity_magnitude = vector_length(target_velocity)
    steps_till_velocity_expected = math.ceil(velocity_magnitude / time_frame)
    num_steps = orientation_steps + steps_till_velocity_expected
    distance_covered = velocity_magnitude * num_steps
    court = create_court(width=distance_covered, height=distance_covered)
    game = create_game(teams=create_teams(player), court=court).assign_team_strategy(
        0, UseBehavior(ReachVelocity(target_velocity))
    )
    space = create_space().add(game)
    for _ in range(num_steps):
        space.step(time_frame)
    assert close_to(player.velocity, target_velocity)


def setup_collision_with_use_behavior(
    distance: float, mass_1: float, mass_2: float
) -> Game:
    assert distance > mass_1 + mass_2
    court = create_court(width=distance + 4)
    player_1 = create_initialized_player(
        attributes=create_player_attributes(size=1.0, mass=mass_1),
        position=(court.width / 2 - distance / 2, court.height / 2),
    )
    player_2 = create_initialized_player(
        attributes=create_player_attributes(size=1.0, mass=mass_2),
        position=(court.width / 2 + distance / 2, court.height / 2),
        orientation_degrees=-180,
    )
    assert approx(abs(player_1.position[0] - player_2.position[0]), distance)
    assert approx(abs(player_1.position[1] - player_2.position[1]), 0.0)

    game = create_game(create_teams(player_1, player_2))
    game.assign_team_strategy(0, UseBehavior(ReachVelocity((1, 0))))
    game.assign_team_strategy(1, UseBehavior(ReachVelocity((-1, 0))))
    return game


@pytest.mark.parametrize(
    "distance_player_masses",
    [(7, 1.0, 2.0), (7, 2.0, 1.0), (7, 1.0, 1.0), (7, 2.0, 2.0)],
)
def test_collision_with_use_behavior(
    distance_player_masses: Tuple[float, float, float]
):
    time_frame = 0.2
    distance, mass_1, mass_2 = distance_player_masses
    game = setup_collision_with_use_behavior(distance, mass_1, mass_2)
    space = create_space(game)
    [player_1], [player_2] = game.teams
    steps_to_push_off_court = math.ceil(2 * game.court.width / time_frame)
    for _ in range(steps_to_push_off_court):
        space.step(time_frame)
    expected_inbounds = approx(mass_1, mass_2)
    assert game.court.is_inbounds(player_1) == expected_inbounds
    assert game.court.is_inbounds(player_2) == expected_inbounds


def test_scoring_with_composite_strategy():
    duration = 50
    time_frame = 1 / 30
    attributes = create_player_attributes(
        shot_probability=create_guaranteed_shot_probability()
    )
    player_1 = create_initialized_player(position=(4, 4), attributes=attributes)
    player_2 = create_initialized_player(position=(7, 7), attributes=attributes)
    hoop = create_hoop(offset_from_left=0.2)
    court = create_court(hoop=hoop)
    game = create_game(teams=create_teams(player_1, player_2), court=court)
    space = create_space().add(game)
    for team_index in range(2):
        game.assign_team_strategy(team_index, create_strategy(0.1))
    num_steps = math.ceil(duration / time_frame)
    for _ in range(num_steps):
        space.step(time_frame)
    assert game.score[0] > 0 and game.score[1] > 0


def setup_stay_relatively_on_court_with_composite_strategy(player_size) -> Game:
    width, height = 28, 15
    offset_from_left = 2 if player_size == 0 else 2 * player_size + 0.5
    attributes = create_player_attributes(
        shot_probability=create_guaranteed_shot_probability(),
        max_acceleration=2.5,
        size=player_size,
    )
    player_1 = create_initialized_player(position=(4, 4), attributes=attributes)
    player_2 = create_initialized_player(position=(7, 7), attributes=attributes)
    hoop = create_hoop(width, height, offset_from_left=offset_from_left)
    court = create_court(width, height, hoop)
    game = create_game(teams=create_teams(player_1, [player_2]), court=court)
    game.assign_team_strategy(0, create_strategy(5))
    game.assign_team_strategy(1, create_strategy(3))
    return game


@pytest.mark.parametrize("player_size", [0.0, 0.5, 1.0])
def test_stay_relatively_on_court_with_composite_strategy(player_size):
    duration = 50
    time_frame = 1 / 30
    num_steps = math.ceil(duration / time_frame)
    game = setup_stay_relatively_on_court_with_composite_strategy(player_size)
    player_1, player_2 = game.teams[0][0], game.teams[1][0]
    space = create_space().add(game)

    threshold = 1
    for _ in range(num_steps):
        assert_relatively_on_court(game.court, player_1, threshold)
        assert_relatively_on_court(game.court, player_2, threshold)
        space.step(time_frame)


def test_stay_close_with_composite_strategy():
    duration = 50
    time_frame = 1 / 30
    num_steps = math.ceil(duration / time_frame)
    attributes = create_player_attributes(
        max_acceleration=2, max_turn_degrees=480, velocity_decay=0.001
    )
    width = 20
    height = 15
    player_1 = create_initialized_player(
        position=(4, height / 2 + 0.5), attributes=attributes
    )
    player_2 = create_initialized_player(
        position=(4, height / 2 - 0.5), attributes=attributes
    )
    hoop = create_hoop(width, height, offset_from_left=2)
    court = create_court(width, height, hoop)
    game = create_game(teams=create_teams([player_1], player_2), court=court)
    game.assign_team_strategy(0, create_strategy(0.01))
    game.assign_team_strategy(1, create_strategy(0.01))
    space = create_space().add(game)

    threshold = 1.8
    # First, get into steady state where players trail behind each other
    for _ in range(num_steps):
        space.step(time_frame)
    for _ in range(num_steps):
        assert close_to(player_1.position, player_2.position, threshold)
        space.step(time_frame)


def setup_eventual_inbounds_with_everyone_initially_out_of_bounds(
    initial_error: float,
) -> Game:
    width = 20
    height = 10
    attributes = create_player_attributes(size=1.0)
    player_1 = create_initialized_player(
        position=(-initial_error, height + initial_error), attributes=attributes
    )
    player_2 = create_initialized_player(
        position=(width + initial_error, -initial_error), attributes=attributes
    )
    court = create_court(width, height)
    game = create_game(teams=create_teams(player_1, player_2), court=court)
    game.assign_team_strategy(0, create_strategy(5))
    game.assign_team_strategy(1, create_strategy(5))
    return game


def test_eventual_inbounds_with_everyone_initially_out_of_bounds():
    duration = 10
    time_frame = 1 / 20
    num_steps = math.ceil(duration / time_frame)
    game = setup_eventual_inbounds_with_everyone_initially_out_of_bounds(2.0)
    space = create_space().add(game)
    for _ in range(num_steps):
        space.step(time_frame)
    assert game.score[0] > 0 or game.score[1] > 0


def setup_consistent_inbounds_despite_collisions(
    mass_2: float, use_expected_value: bool
):
    size = 0.9
    max_acceleration = 2.34
    max_turn_degrees = 360
    velocity_decay = 0.005
    width = 28.65
    height = 15.24
    player_1 = create_initialized_player(
        position=(4, height / 2),
        attributes=create_player_attributes(
            size=size,
            max_acceleration=max_acceleration,
            max_turn_degrees=max_turn_degrees,
            velocity_decay=velocity_decay,
        ),
    )
    player_2 = create_initialized_player(
        position=(8, height / 2),
        attributes=create_player_attributes(
            mass=mass_2,
            size=size,
            max_acceleration=max_acceleration,
            max_turn_degrees=max_turn_degrees,
            velocity_decay=velocity_decay,
        ),
    )
    hoop = create_hoop(width, height, 1.6, create_three_point_line(width, height))
    court = create_court(width, height, hoop)
    game = create_game(
        teams=create_teams(player_1, player_2),
        court=court,
        settings=create_game_settings(use_expected_value_for_points=use_expected_value),
    )
    game.assign_team_strategy(0, create_strategy(1))
    game.assign_team_strategy(1, create_strategy(20))
    return game


def test_consistent_inbounds_despite_collisions():
    duration = 800
    time_frame = 1 / 5
    num_steps = math.ceil(duration / time_frame)
    game = setup_consistent_inbounds_despite_collisions(2.0, True)
    space = create_space(game)
    [player_1], [player_2] = game.teams
    threshold = game.court.width / 5
    for _ in range(num_steps):
        assert_relatively_on_court(game.court, player_1, threshold)
        assert_relatively_on_court(game.court, player_2, threshold)
        space.step(time_frame)
    assert game.score[0] > 0 and game.score[1] > 0
