from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Optional, List, Tuple, Callable


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

    @staticmethod
    def create(
        game_generator: Callable[[], Any],
        population_size: int,
        generation_limit: Optional[int],
        *,
        duration: float,
        fps: int,
        speed_scale: float,
    ) -> Metadata:
        game = game_generator()
        teams = tuple(
            TeamMetadata(
                [asdict(player._attributes) for player in game.teams[team_index]],
                team_index,
            )
            for team_index in range(2)
        )
        return Metadata(
            (teams[0], teams[1]),
            population_size,
            generation_limit,
            duration,
            fps,
            speed_scale,
        )
