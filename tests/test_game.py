from bball_server import BallMode
from .utils import (
    create_initialized_player,
    create_space,
    create_game,
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
