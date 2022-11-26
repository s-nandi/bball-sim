from tests.utils import (
    create_space,
    create_player_attributes,
    create_initialized_player,
    close_to,
)


def test_if_displaced():
    player = create_initialized_player()
    space = create_space().add(player)

    original_position = player.position
    player.turn(1).accelerate(1)
    assert close_to(player.position, original_position)
    space.step(1)
    assert not close_to(player._physics._body.position, original_position)


def test_accelerate_simple():
    player = create_initialized_player(create_player_attributes())
    space = create_space().add(player)
    player.accelerate(1)
    space.step(1)
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))


def test_skip_accelerate():
    player = create_initialized_player(
        create_player_attributes(max_acceleration=2.0, velocity_decay=0)
    )
    space = create_space().add(player)

    player.turn(1)
    space.step(1)
    player.accelerate(0.5)
    space.step(1)

    body = player._physics._body
    print(player, body.force, len(body.space.bodies), body.mass)

    assert close_to(player.position, (0, 1))
    assert close_to(player.velocity, (0, 1))
    space.step(1)
    assert close_to(player.position, (0, 2))
    assert close_to(player.velocity, (0, 1))


def test_accelerate_twice():
    player = create_initialized_player(
        create_player_attributes(max_acceleration=2.0, velocity_decay=0)
    )
    space = create_space().add(player)

    player.turn(1)
    space.step(1)
    player.accelerate(0.5)
    space.step(1)
    assert close_to(player.position, (0, 1))
    assert close_to(player.velocity, (0, 1))
    player.accelerate(0.5)
    space.step(1)
    assert close_to(player.position, (0, 3))
    assert close_to(player.velocity, (0, 2))


def test_max_velocity_decay():
    player = create_initialized_player(
        create_player_attributes(max_acceleration=1.0, velocity_decay=1.0)
    )
    space = create_space().add(player)

    player.accelerate(1)
    space.step(1)
    assert close_to(player.position, (1, 0))
    player.accelerate(1)
    space.step(1)
    assert close_to(player.position, (2, 0))


def test_velocity_after_turning():
    player = create_initialized_player()
    space = create_space().add(player)

    player.accelerate(1)
    space.step(1)
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (0, 1))
    assert close_to(player.position, (1, 1))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (-1, 0))
    assert close_to(player.position, (0, 1))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (0, -1))
    assert close_to(player.position, (0, 0))
    player.turn(1)
    space.step(1)
    assert close_to(player.velocity, (1, 0))
    assert close_to(player.position, (1, 0))
