import math
import pytest
from bball import BallMode
from bball.strategy import RunToBasketAndShoot, StandBetweenBasket
from bball.utils import distance_between, close_to
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
)


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


def setup_stay_relatively_on_court_with_composite_strategy(player_size):
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

    def assert_relatively_on_court(player, threshold: float):
        position_x = player.position[0]
        position_y = player.position[1]
        assert position_x >= -threshold
        assert position_x <= game.court.width + threshold
        assert position_y >= -threshold
        assert position_y <= game.court.height + threshold

    threshold = 1
    for _ in range(num_steps):
        assert_relatively_on_court(player_1, threshold)
        assert_relatively_on_court(player_2, threshold)
        space.step(time_frame)


def test_stay_close_with_composite_strategy():
    duration = 50
    time_frame = 1 / 30
    num_steps = math.ceil(duration / time_frame)
    attributes = create_player_attributes(max_acceleration=2, max_turn_degrees=480)
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


def setup_eventual_inbounds_with_everyone_initially_out_of_bounds():
    width = 20
    height = 10
    attributes = create_player_attributes(size=1.0)
    initial_error = 2
    player_1 = create_initialized_player(
        position=(-initial_error, -initial_error), attributes=attributes
    )
    player_2 = create_initialized_player(
        position=(width + initial_error, height + initial_error), attributes=attributes
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
    game = setup_eventual_inbounds_with_everyone_initially_out_of_bounds()
    space = create_space().add(game)
    for _ in range(num_steps):
        space.step(time_frame)
    assert game.score[0] > 0 or game.score[1] > 0
