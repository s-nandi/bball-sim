from bball_server import Ball
from .utils import create_initialized_player, create_space, close_to


def test_ball_initial_position():
    player = create_initialized_player()
    ball = Ball()
    ball.give_to(player)
    assert close_to(ball.position, player.position)


def test_ball_sticks_to_player():
    player = create_initialized_player()
    ball = Ball()
    ball.give_to(player)
    space = create_space().add(ball, player)
    player.accelerate(1)
    num_steps = 5
    for _ in range(num_steps):
        space.step(1)
        assert close_to(ball.position, player.position)
