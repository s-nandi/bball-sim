import math
from bball.game import Game
from bball.create import create_space


def compare(
    game: Game,
    duration: float,
    time_frame: float = 0.1,
) -> bool:
    space = create_space(game)
    num_steps = math.ceil(duration / time_frame)
    for _ in range(num_steps):
        space.step(time_frame)
    while game.possessions[0] > game.possessions[1]:
        space.step(time_frame)
    while game.possessions[0] <= game.possessions[1]:
        space.step(time_frame)
    print("final score", game.score)
    print("final possessions", game.possessions)
    return game.score[0] > game.score[1]
