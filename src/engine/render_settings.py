from dataclasses import dataclass
from typing import Tuple


@dataclass
class RenderSettings:
    resolution: Tuple[float, float]
    frame_rate: int
