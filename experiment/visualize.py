from pprint import pprint
from runner import run_game
from experiment.monitor import Monitor
from bball import Game


def visualize(game: Game, fps: float, speed_scale: float, display_scale: float):
    monitor = Monitor(float("inf"))
    run_game(
        game,
        fps=fps,
        speed_scale=speed_scale,
        display_scale=display_scale,
        monitor=lambda: monitor.monitor(game),
    )
    pprint(monitor.stats())
