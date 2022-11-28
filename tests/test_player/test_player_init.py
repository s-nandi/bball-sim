from ..utils import (
    create_initialized_player,
    create_uninitialized_player,
    close_to,
    require_exception,
)


def test_invalid_moves():
    def test_turn(value):
        player = create_initialized_player()
        player.turn(value)

    def test_acceleration(value):
        player = create_initialized_player()
        player.accelerate(value)

    require_exception(lambda: test_turn(1.01), AssertionError)
    require_exception(lambda: test_turn(-1.01), AssertionError)
    require_exception(lambda: test_acceleration(1.01), AssertionError)
    require_exception(lambda: test_acceleration(-1.01), AssertionError)


def test_player_action_order():
    def turn_after_accelerate():
        player = create_initialized_player()
        player.accelerate(1).turn(1)

    def accelerate_after_turn():
        player = create_initialized_player()
        player.turn(1).accelerate(1)

    require_exception(turn_after_accelerate, AssertionError)
    accelerate_after_turn()


def test_place_at():
    player = create_uninitialized_player()
    player.place_at((-100.0, 23), 81)
    assert close_to(player.position, (-100.0, 23))


def test_player_usage_before_init():
    player = create_uninitialized_player()

    def accelerate():
        player.accelerate(1)

    def turn():
        player.turn(1)

    def pass_to():
        receiver = create_initialized_player(position=(1, 1))
        player.pass_to(receiver, pass_velocity=1)

    def shoot_at():
        player.shoot_at((1, 1), shot_velocity=1)

    require_exception(accelerate, AssertionError)
    require_exception(turn, AssertionError)
    require_exception(pass_to, AssertionError)
    require_exception(shoot_at, AssertionError)
