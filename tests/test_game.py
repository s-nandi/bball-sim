from bball_server import BallMode
from .utils import (
    create_initialized_player,
    create_space,
    create_game,
    create_court,
    create_hoop,
    close_to,
    create_uninitialized_player,
)


def test_game_flow():
    player_1 = create_initialized_player()
    player_2 = create_initialized_player()
    game = create_game(teams=([player_1], [player_2]))
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
    game = create_game(teams=([player_1, player_2], []))
    space = create_space().add(game)
    ball = game.ball
    ball.jump_ball_won_by(player_1)
    player_1.pass_to(player_2, 10)
    assert not player_1.has_ball
    assert not player_2.has_ball
    assert ball.mode == BallMode.MIDPASS
    space.step(1)
    assert ball.mode == BallMode.POSTPASS
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
    game = create_game(teams=([player], []), court=court)
    ball = game.ball
    ball.jump_ball_won_by(player)
    target_position = game.target_hoop(player).position
    player.shoot_at(target_position, 0.5)
    assert close_to(player.position, (0, height / 2))
    assert close_to(target_position, (width, height / 2))
    player.accelerate(1)
    space = create_space().add(game)
    for time_since_shot in range(width * 2):
        assert ball.mode == BallMode.MIDSHOT
        assert close_to(ball.position, (time_since_shot / 2, height / 2))
        space.step(1)
    assert ball.mode == BallMode.POSTSHOT
    space.step(0)
    assert ball.mode == BallMode.DEAD


def test_scoring():
    player_1 = create_uninitialized_player()
    player_2 = create_uninitialized_player()
    game = create_game(teams=([player_1], [player_2]))
    ball = game.ball
    court = game.court
    player_1.place_at((0, court.height / 2), 0)
    player_2.place_at((court.width, court.height / 2), 0)
    space = create_space().add(game)
    ball.jump_ball_won_by(player_1)
    assert player_1.has_ball
    assert not player_2.has_ball
    player_1.shoot_at(game.target_hoop(player_1).position, 1)
    assert ball.mode == BallMode.MIDSHOT
    for _ in range(court.width):
        space.step(1)
    assert ball.mode == BallMode.POSTSHOT
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
    player_2.shoot_at(game.target_hoop(player_2).position, 0.0001)
    assert ball.mode == BallMode.MIDSHOT
    space.step(0)
    assert ball.mode == BallMode.POSTSHOT
    space.step(0)
    assert ball.mode == BallMode.DEAD
    assert game.score == (3, 2)
