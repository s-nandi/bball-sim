from bball import Game, Space, draw_game
from engine import Engine
from runner.draw import Drawer, resolution_for, padded_resolution_for

GRAYSCALE = 230
BACKGROUND_COLOR = (GRAYSCALE, GRAYSCALE, GRAYSCALE)


def loop(game: Game, engine: Engine, drawer: Drawer, time_step: float):
    space = Space().add(game)

    def _loop():
        drawer.surface.fill(BACKGROUND_COLOR)
        draw_game(drawer, game)

        target_rectangle = engine.surface.get_rect()
        source_rectangle = drawer.surface.get_rect(center=target_rectangle.center)
        engine.surface.blit(drawer.surface, source_rectangle)

        space.step(time_step)

    return _loop


def run_game(game: Game, fps: int, display_scale: float, monitor=None):
    resolution = resolution_for(game, display_scale)
    padded_resolution = padded_resolution_for(game, display_scale, display_scale)
    scale = resolution[0] / game.court.dimensions[0]
    padding = (padded_resolution[0] - resolution[0]) / 2

    drawer = Drawer(padded_resolution, scale, (padding, padding))
    engine = Engine(padded_resolution, fps)
    main_loop = loop(game, engine, drawer, 1 / fps)

    def game_loop():
        if monitor is not None:
            monitor()
        main_loop()

    engine.run(game_loop)
