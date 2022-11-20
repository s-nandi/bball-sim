import pymunk
import pymunk.pygame_util
from simulation.types import TimePerFrame, Fps, SpeedScale


class SimulationParams:
    space: pymunk.Space
    time_per_frame: TimePerFrame

    def __init__(
        self,
        fps: Fps,
        speed_scale: SpeedScale = 1.0,
    ):
        self.space = pymunk.Space()
        pymunk.pygame_util.positive_y_is_up = True
        self.time_per_frame = speed_scale / fps
