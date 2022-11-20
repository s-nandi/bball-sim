import dataclasses
from simulation.types import ScreenDimension, Fps


@dataclasses.dataclass
class ScreenParams:
    width: ScreenDimension
    height: ScreenDimension
    fps: Fps
