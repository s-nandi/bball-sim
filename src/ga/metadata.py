from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Metadata:
    teams: Any
    population_size: int
    generation_limit: Optional[int]
