import dataclasses
from visualizer.types import ScreenDimension, Fps


@dataclasses.dataclass
class ScreenParams:
    width: ScreenDimension
    height: ScreenDimension
    fps: Fps
