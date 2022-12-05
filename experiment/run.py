from pprint import pprint
from runner import run, run_headless
from experiment.monitor import Monitor
from bball import Game


def visualize(game: Game, fps: int, speed_scale: float, display_scale: float):
    monitor = Monitor(float("inf"))
    run(
        game,
        fps=fps,
        speed_scale=speed_scale,
        display_scale=display_scale,
        monitor=lambda: monitor.monitor(game),
    )
    pprint(monitor.stats())


def headless(game: Game, fps: int, speed_scale: float, duration: float):
    monitor = Monitor(float("inf"))
    run_headless(
        game,
        fps=fps,
        speed_scale=speed_scale,
        duration=duration,
        monitor=lambda: monitor.monitor(game),
    )
    pprint(monitor.stats())
