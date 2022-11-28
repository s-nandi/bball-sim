from bball_server import Game, BallMode
from .utils import create_ball, create_initialized_player, create_court, create_space


def test_game_flow():
    player_1 = create_initialized_player()
    player_2 = create_initialized_player()
    ball = create_ball()
    court = create_court()
    game = Game(([player_1], [player_2]), ball, court)
    space = create_space().add(game)

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
