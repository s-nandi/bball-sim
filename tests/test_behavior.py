from random import uniform, choice
import pytest
from bball_server import Team, Teams, ReachVelocityBehavior, StopBehavior
from bball_server.utils import close_to, approx
from .utils import create_initialized_player, create_space


def test_steady_velocity_behavior():
    steps = 10
    player = create_initialized_player()
    space = create_space().add(player)
    target_velocity = (-2, 2)
    behavior = ReachVelocityBehavior(target_velocity)
    for _ in range(steps):
        behavior.drive(player)
        space.step(1)
    assert close_to(player.velocity, target_velocity)


@pytest.mark.parametrize("_trial_index", range(60))
def test_steady_velocity_behavior_with_initial_movement(_trial_index):
    initial_steps = choice([1, 10, 50])
    team = Team(create_initialized_player())
    space = create_space().add(team)
    for _ in range(initial_steps):
        team[0].turn(uniform(0, 1)).accelerate(1)
        space.step(1)
    target_velocity_x = choice([-2, 2])
    extra_steps_for_rotation = 2 if target_velocity_x < 0 else 0
    extra_steps_for_velocity = abs(target_velocity_x)
    target_velocity = (target_velocity_x, 0)
    behavior = ReachVelocityBehavior(target_velocity)
    for _ in range(initial_steps + extra_steps_for_rotation + extra_steps_for_velocity):
        behavior.drive(team[0])
        space.step(1)
    assert close_to(team[0].velocity, target_velocity)


@pytest.mark.parametrize("_trial_index", range(60))
def test_stopping_behavior(_trial_index):
    initial_steps = choice([2, 10, 50])
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
    behavior = StopBehavior()
    for _ in range(initial_steps):
        behavior.drive(player_1)
        behavior.drive(player_2)
        space.step(1)
    target_velocity = (0, 0)
    assert close_to(player_1.velocity, target_velocity)
    assert close_to(player_2.velocity, target_velocity)
