import math
from dataclasses import dataclass
from bball_server import BallMode, Scoreboard, Team
from bball_server.utils import close_to, distance_between, approx
from bball_server.create import (
    create_initialized_player,
    create_space,
    create_game_settings,
    create_game,
    create_court,
    create_hoop,
    create_uninitialized_player,
    create_guaranteed_shot_probability,
    create_player_attributes,
)


def test_game_flow():
    player_1 = create_initialized_player()
    player_2 = create_initialized_player()
    game = create_game(teams=[Team(player_1), Team(player_2)])
    space = create_space().add(game)
    ball = game.ball

    def test_running_out_of_bounds():
        ball.jump_ball_won_by(player_1)
        assert ball.mode == BallMode.HELD
        player_1.turn(-1).accelerate(1)
        space.step(0)
        assert ball.mode == BallMode.HELD
        player_1.turn(-1).accelerate(1)
        space.step(0.0001)
        assert ball.mode == BallMode.DEAD

    def test_arbitrary_inbound():
        space.step(0)
        assert ball.mode == BallMode.HELD
        assert player_2.has_ball

    test_running_out_of_bounds()
    test_arbitrary_inbound()


def test_pass_completion():
    player_1 = create_initialized_player()
    player_2 = create_initialized_player(position=(3, 3))
    game = create_game(teams=[Team(player_1, player_2)])
    space = create_space().add(game)
    ball = game.ball
    ball.jump_ball_won_by(player_1)
    player_1.pass_to(player_2, 10)
    space.step(0)
    assert not player_1.has_ball
    assert not player_2.has_ball
    assert ball.mode == BallMode.MIDPASS
    space.step(1)
    assert ball.mode == BallMode.RECEIVEDPASS
    space.step(0)
    assert ball.mode == BallMode.HELD
    assert player_2.has_ball


def test_shot_completion_with_movement_after_shot():
    width = 10
    height = 6
    hoop = create_hoop(width, height)
    assert close_to(hoop.position, (0, height / 2))
    court = create_court(width, height, hoop)
    player = create_initialized_player(position=(0, height / 2))
    game = create_game(teams=[Team(player)], court=court)
    space = create_space().add(game)
    ball = game.ball
    ball.jump_ball_won_by(player)
    target_position = game.target_hoop(player).position
    player.shoot_at(target_position, 0.5)
    space.step(0)
    assert close_to(player.position, (0, height / 2))
    assert close_to(target_position, (width, height / 2))
    player.accelerate(1)
    for time_since_shot in range(width * 2):
        assert ball.mode == BallMode.MIDSHOT
        assert close_to(ball.position, (time_since_shot / 2, height / 2))
        space.step(1)
        assert not close_to(ball.position, player.position)
    assert ball.mode == BallMode.REACHEDSHOT
    space.step(0)
    assert ball.mode == BallMode.DEAD


def test_scoring():
    guaranteed_scorer_attributes = create_player_attributes(
        shot_probability=create_guaranteed_shot_probability()
    )
    player_1 = create_uninitialized_player(attributes=guaranteed_scorer_attributes)
    player_2 = create_uninitialized_player(attributes=guaranteed_scorer_attributes)
    game = create_game(teams=[Team(player_1), Team(player_2)])
    space = create_space().add(game)
    ball = game.ball
    court = game.court
    player_1.place_at((0, court.height / 2), 0)
    player_2.place_at((court.width, court.height / 2), 0)
    ball.jump_ball_won_by(player_1)
    assert player_1.has_ball
    assert not player_2.has_ball
    player_1.shoot_at(game.target_hoop(player_1).position, 1)
    space.step(0)
    assert ball.mode == BallMode.MIDSHOT
    for _ in range(court.width):
        space.step(1)
    assert ball.mode == BallMode.REACHEDSHOT
    space.step(0)
    assert ball.mode == BallMode.DEAD
    space.step(0)
    assert ball.mode == BallMode.HELD
    assert not player_1.has_ball
    assert player_2.has_ball
    assert game.score == (3, 0)
    player_2.accelerate(-1)
    for _ in range(court.width):
        space.step(1)
    player_2_target = game.target_hoop(player_2)
    assert close_to(player_2.position, player_2_target.position)
    player_2.shoot_at(player_2_target.position, 0.0001)
    space.step(0)
    assert ball.mode == BallMode.REACHEDSHOT
    space.step(0)
    assert ball.mode == BallMode.DEAD
    assert game.score == (3, 2)


@dataclass
class ScoringTest:
    score: Scoreboard
    concrete_value: int
    expected_value: float


def _check_probability_in_threshold(
    probability: float, lower_bound: float, upper_bound: float
):
    rounded_probability = round(probability, 2)
    unsafe_probability_msg = (
        f"Want shot probability between {lower_bound} and {upper_bound}"
        f" but have p={rounded_probability}, change court dimensions to fix"
    )
    assert lower_bound <= rounded_probability <= upper_bound, unsafe_probability_msg


def setup_scoring_test(use_ev: bool) -> ScoringTest:
    width = 50
    court = create_court(width=width)
    player = create_initialized_player()
    game = create_game(
        teams=[Team(player)], settings=create_game_settings(use_ev), court=court
    )
    ball = game.ball
    space = create_space().add(game)
    ball.jump_ball_won_by(player)
    target_hoop = game.target_hoop(player)
    distance_to_target = distance_between(player.position, target_hoop.position)
    concrete_value = target_hoop.value_of_shot_from(player.position)
    probability = player._attributes.skill.shot_probability.probability(
        distance_to_target
    )
    _check_probability_in_threshold(probability, 0.45, 0.55)
    expected_value = concrete_value * probability
    player.shoot_at(target_hoop.position, 1)
    space.step(0)
    for _ in range(math.ceil(distance_to_target)):
        assert ball.mode == BallMode.MIDSHOT
        space.step(1)
    assert ball.mode == BallMode.REACHEDSHOT
    space.step(0)
    return ScoringTest(game.score, concrete_value, expected_value)


def test_expected_value_scoring():
    test = setup_scoring_test(use_ev=True)
    assert approx(test.score[0], test.expected_value)
    assert test.score[1] == 0


def test_non_guaranteed_scoring():
    trials = 100
    times_scored = 0
    for _ in range(trials):
        test = setup_scoring_test(use_ev=False)
        assert test.score[0] in (0, 2, 3)
        assert test.score[1] == 0
        did_score = test.score[0] > 0
        if did_score:
            times_scored += 1
    assert 0 < times_scored < trials
