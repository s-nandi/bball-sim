from experiment.initiate import canonical_game
from bball import Player
from bball.utils import divide_by

canonical_court = canonical_game(0).court
bigger_dimension = max(canonical_court.dimensions)


def court_dimensions():
    width, height = canonical_court.dimensions
    return width / bigger_dimension, height / bigger_dimension


def velocity(player: Player):
    velocity = player.velocity
    return divide_by(velocity, bigger_dimension)


def position(player: Player):
    position = player.position
    return divide_by(position, bigger_dimension)
