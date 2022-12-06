from dataclasses import dataclass
from typing import Any, Optional, List, Tuple


@dataclass
class TeamMetadata:
    player_attributes: List[Any]
    team_index: int


@dataclass
class Metadata:
    teams: Tuple[TeamMetadata, TeamMetadata]
    population_size: int
    generation_limit: Optional[int]
    duration: float
    fps: int
    speed_scale: float
