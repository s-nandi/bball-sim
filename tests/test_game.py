from bball_server import Game, BallMode
from .utils import (
    create_ball,
    create_initialized_player,
    create_court,
    create_space,
    close_to,
)


def test_running_out_of_bounds():
    player = create_initialized_player()
    ball = create_ball()
    court = create_court()
    game = Game(([player], []), ball, court)
    space = create_space().add(game)
    ball.jump_ball_won_by(player)
    assert ball.mode == BallMode.HELD
    player.turn(-1).accelerate(1)
    space.step(1)
    assert close_to(player.position, (0, -1))
    assert ball.mode == BallMode.DEAD
