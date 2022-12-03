from bball import Game, Space, draw_game
from engine import Engine
from runner.draw import Drawer, max_resolution_for


def loop(game: Game, drawer: Drawer, time_step: float):
    space = Space().add(game)

    def _loop():
        draw_game(drawer, game)
        space.step(time_step)

    return _loop


def run_game(game: Game, fps: int):
    resolution = max_resolution_for(game)
    engine = Engine(resolution, fps)
    drawer = Drawer(engine.surface, resolution[0] / game.court.dimensions[0])
    callback = loop(game, drawer, 1 / fps)
    engine.run(callback)
