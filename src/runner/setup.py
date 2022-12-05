import math
from bball import Game, Space, draw_game
from engine import Engine
from runner.draw import Drawer, resolution_for, padded_resolution_for

GRAYSCALE = 230
BACKGROUND_COLOR = (GRAYSCALE, GRAYSCALE, GRAYSCALE)

MAX_SUBSTEP_LENGTH = 0.01


def time_frame_for(fps: int, speed_scale: float) -> float:
    return speed_scale / fps


def step_space(space: Space, time_frame: float):
    space.step(time_frame, MAX_SUBSTEP_LENGTH)


def loop(game: Game, engine: Engine, drawer: Drawer, time_frame: float):
    space = Space().add(game)

    def _loop():
        drawer.surface.fill(BACKGROUND_COLOR)
        draw_game(drawer, game)

        target_rectangle = engine.surface.get_rect()
        source_rectangle = drawer.surface.get_rect(center=target_rectangle.center)
        engine.surface.blit(drawer.surface, source_rectangle)
        step_space(space, time_frame)

    return _loop


def run(game: Game, fps: int, speed_scale: float, display_scale: float, monitor=None):
    resolution = resolution_for(game, display_scale)
    padded_resolution = padded_resolution_for(game, display_scale, display_scale)
    scale = resolution[0] / game.court.dimensions[0]
    padding = (padded_resolution[0] - resolution[0]) / 2

    drawer = Drawer(padded_resolution, scale, (padding, padding))
    engine = Engine(padded_resolution, fps)
    main_loop = loop(game, engine, drawer, time_frame_for(fps, speed_scale))

    def game_loop():
        if monitor is not None:
            monitor()
        main_loop()

    engine.run(game_loop)


def run_headless(
    game: Game, fps: int, speed_scale: float, duration: float, monitor=None
) -> Game:
    time_frame = time_frame_for(fps, speed_scale)
    space = Space().add(game)
    num_steps = math.ceil(duration / time_frame)

    def game_loop():
        if monitor is not None:
            monitor()
        step_space(space, time_frame)

    for _ in range(num_steps):
        game_loop()
    return game
