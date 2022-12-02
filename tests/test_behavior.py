import math
from random import uniform, seed
import pytest
from bball import (
    Team,
    Teams,
    ReachVelocityBehavior,
    StopBehavior,
    ReachPositionBehavior,
)
from bball.utils import close_to, approx
from bball.create import create_initialized_player, create_space

seed(1)


def test_steady_velocity_behavior():
    steps = 10
    player = create_initialized_player()
    space = create_space().add(player)
    target_velocity = (-2, 2)
    time_frame = 1
    behavior = ReachVelocityBehavior(target_velocity, time_frame)
    for _ in range(steps):
        if not behavior.drive(player):
            break
        space.step(time_frame)
    assert close_to(player.velocity, target_velocity)


@pytest.mark.parametrize("_trial_index", range(10))
@pytest.mark.parametrize("initial_steps", (1, 10, 50))
@pytest.mark.parametrize("target_velocity_x", (-2, 2))
def test_steady_velocity_behavior_with_initial_movement(
    _trial_index, initial_steps, target_velocity_x
):
    team = Team(create_initialized_player())
    space = create_space().add(team)
    time_frame = 0.2
    for _ in range(initial_steps):
        team[0].turn(uniform(0, 1)).accelerate(1)
        space.step(time_frame)
    rotation_steps = 2 if target_velocity_x < 0 else 0
    acceleration_steps = abs(target_velocity_x)
    target_velocity = (target_velocity_x, 0)
    behavior = ReachVelocityBehavior(target_velocity, time_frame)
    allowed_steps = initial_steps + (rotation_steps + acceleration_steps) / time_frame
    for _ in range(math.ceil(allowed_steps)):
        if not behavior.drive(team[0]):
            break
        space.step(time_frame)
    assert close_to(team[0].velocity, target_velocity)


@pytest.mark.parametrize("_trial_index", range(20))
@pytest.mark.parametrize("initial_steps", (2, 10, 50))
def test_stopping_behavior(_trial_index, initial_steps):
    teams = Teams(
        Team(create_initialized_player(position=(0, 0))),
        Team(create_initialized_player(position=(0, 5))),
    )
    space = create_space().add(teams)
    player_1 = teams[0][0]
    player_2 = teams[1][0]
    player_2.turn(1 / 90)
    for _ in range(initial_steps):
        player_1.accelerate(uniform(-1, -0.1))
        player_2.accelerate(uniform(0.9, 1))
        space.step(1)
    assert approx(player_1.orientation_degrees, 0)
    assert approx(player_2.orientation_degrees, 1)
    assert player_1.velocity[0] < 0
    assert player_2.velocity[0] > 0
    time_frame = 1
    behavior = StopBehavior(time_frame)
    for _ in range(initial_steps):
        moved_1 = behavior.drive(player_1)
        moved_2 = behavior.drive(player_2)
        if not moved_1 and not moved_2:
            break
        space.step(time_frame)
    target_velocity = (0, 0)
    assert close_to(player_1.velocity, target_velocity)
    assert close_to(player_2.velocity, target_velocity)


TARGET_POSITIONS = [
    (1.2, 0),
    (1.21, 0),
    (4.5, 0.001),
    (4.5, 3),
    (3, 4.5),
    (-5, 0),
    (-5, 1),
    (-5, -5),
    (0, 5),
    (0, -5),
    (1.1, -4.2),
]


@pytest.mark.parametrize("target_position", TARGET_POSITIONS)
def test_position_reaching(target_position):
    player = create_initialized_player()
    space = create_space().add(player)
    time_frame = 0.2
    behavior = ReachPositionBehavior(target_position, time_frame)
    turn_steps = 360 / player.physical_attributes.max_turn_degrees / time_frame
    acceleration_steps = math.hypot(target_position[0], target_position[1]) / time_frame
    allowed_steps = turn_steps + acceleration_steps
    for _ in range(math.ceil(allowed_steps)):
        if not behavior.drive(player):
            break
        space.step(time_frame)
    assert close_to(player.velocity, (0, 0))
    assert close_to(player.position, target_position)


@pytest.mark.parametrize("initial_steps", (1, 10, 50))
@pytest.mark.parametrize("target_position", TARGET_POSITIONS)
def test_position_reaching_with_initial_movement(initial_steps, target_position):
    player = create_initialized_player()
    space = create_space().add(player)
    time_frame = 0.2
    behavior = ReachPositionBehavior(target_position, time_frame)
    turn_steps = 360 / player.physical_attributes.max_turn_degrees / time_frame
    acceleration_steps = math.hypot(target_position[0], target_position[1]) / time_frame
    allowed_steps = turn_steps + acceleration_steps + initial_steps
    for _ in range(initial_steps):
        player.turn(uniform(0, 1)).accelerate(uniform(-1, 1))
        space.step(time_frame)
    for _ in range(math.ceil(allowed_steps)):
        if not behavior.drive(player):
            break
        space.step(time_frame)
    assert close_to(player.velocity, (0, 0))
    assert close_to(player.position, target_position)
