from bball_server import Team, SteadyVelocityBehavior
from bball_server.utils import close_to
from .utils import create_initialized_player, create_space


def test_steady_velocity_behavior():
    player = create_initialized_player()
    team = Team(player)
    space = create_space().add(player)
    target_velocity = (-5, 0)
    behavior = SteadyVelocityBehavior(target_velocity)
    for _ in range(30):
        behavior.drive(team)
        space.step(1)
    assert close_to(player.velocity, target_velocity)
