from dataclasses import dataclass
from typing import Tuple


@dataclass
class RenderSettings:
    resolution: Tuple[int, int]
    frame_rate: int
