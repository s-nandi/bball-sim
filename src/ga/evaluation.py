from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Evaluation:
    deltas: List[Tuple[int, int, float]]
    fitness: List[float]
    winners: List[int]
