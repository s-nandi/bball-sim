from ..utils import create_initialized_player, create_space, create_ball


def test_posession_ends_after_shooting():
    player = create_initialized_player()
    ball = create_ball()
    space = create_space().add(player, ball)
    ball.give_to(player)
    player.shoot_at((1, 0))
    space.step(1)
    assert not player.has_ball
