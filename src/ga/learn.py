from __future__ import annotations
import uuid
from dataclasses import asdict
from typing import Optional, List, Callable, TYPE_CHECKING
from tqdm import tqdm
from ga.evaluation_game import evaluation_game
from ga.parameters import (
    Parameters,
    RegularParameters,
    SpacedParameters,
    ParametersSerializer,
    compare,
    combine,
)
from ga.evolution import evolve
from ga.metadata import Metadata, TeamMetadata

if TYPE_CHECKING:
    from bball import Game

    GameGenerator = Callable[[], Game]
    Comparator = Callable[[Parameters, Parameters], bool]


def create_initial_population(population_size: int, width: float) -> List[Parameters]:
    num_init_spaced_parameters = population_size // 2
    num_init_regular_parameters = population_size - num_init_spaced_parameters
    spaced_parameters = [
        SpacedParameters.generate_random(width)
        for _ in range(num_init_spaced_parameters)
    ]
    regular_parameters = [
        RegularParameters.generate_random(width)
        for _ in range(num_init_regular_parameters)
    ]
    return spaced_parameters + regular_parameters


def genalgo(
    gen_id: str,
    game_generator: GameGenerator,
    comparator: Comparator,
    *,
    population_size: int,
    generation_limit: Optional[int],
    output_folder: Optional[str],
    output_frequency: int,
):
    do_serialization = output_folder is not None
    if do_serialization:
        game = game_generator()
        teams = tuple(
            TeamMetadata(
                [asdict(player._attributes) for player in game.teams[team_index]],
                team_index,
            )
            for team_index in range(2)
        )
        metadata = Metadata((teams[0], teams[1]), population_size, generation_limit)
        assert output_folder is not None
        serializer = ParametersSerializer(gen_id, output_folder, output_frequency)
        serializer.serialize_metadata(metadata)

    parameters_list = create_initial_population(
        population_size, game_generator().court.width
    )

    generation_number = 0
    with tqdm(total=generation_limit) as progress_bar:
        while generation_limit is None or generation_number < generation_limit:
            parameters_list = evolve(comparator, combine, parameters_list)
            if do_serialization:
                serializer.serialize_parameters(parameters_list)
            generation_number += 1
            progress_bar.update(1)
    serializer.serialize_parameters(parameters_list, force=True)


DURATION = 50
FPS = 60
SPEED_SCALE = 3.0


def learn(
    num_players: int,
    population_size: int,
    generation_limit: Optional[int] = None,
    output_folder: Optional[str] = None,
    output_frequency: int = 1,
):
    gen_id = str(uuid.uuid1()).replace("-", "")[:16]

    def game_generator() -> Game:
        return evaluation_game(num_players)

    def comparator(parameters_1: Parameters, parameters_2: Parameters):
        game = game_generator()
        return compare(
            game,
            parameters_1,
            parameters_2,
            duration=DURATION,
            fps=FPS,
            speed_scale=SPEED_SCALE,
        )

    genalgo(
        gen_id,
        game_generator,
        comparator,
        population_size=population_size,
        generation_limit=generation_limit,
        output_folder=output_folder,
        output_frequency=output_frequency,
    )
