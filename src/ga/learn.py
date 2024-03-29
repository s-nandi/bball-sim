from __future__ import annotations
import uuid
from typing import Optional, Callable, TYPE_CHECKING
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
from ga.evolution import evolve, tournament, Population
from ga.metadata import Metadata

if TYPE_CHECKING:
    from bball import Game

    GameGenerator = Callable[[], Game]
    Comparator = Callable[[Parameters, Parameters], bool]

DURATION = 100
FPS = 60
SPEED_SCALE = 3.0


def create_initial_population(population_size: int, width: float) -> Population:
    num_types = 2
    while population_size % (2 * num_types) != 0:
        population_size += 1
    individuals_per_type = population_size // num_types
    spaced_parameters: Population = [
        SpacedParameters.generate_random(width) for _ in range(individuals_per_type)
    ]
    regular_parameters: Population = [
        RegularParameters.generate_random(width) for _ in range(individuals_per_type)
    ]
    return list(spaced_parameters) + list(regular_parameters)


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
    serializer = None
    if output_folder is not None:
        serializer = ParametersSerializer(output_folder, gen_id, output_frequency)
        metadata = Metadata.create(
            game_generator,
            population_size,
            generation_limit,
            duration=DURATION,
            fps=FPS,
            speed_scale=SPEED_SCALE,
        )
        serializer.serialize_metadata(metadata)

    def serialize(parameters_list, evaluations, force: bool = False):
        if serializer is not None:
            serializer.serialize_evaluation(evaluations, force)
            serializer.serialize_parameters(parameters_list, force)

    parameters_list = create_initial_population(
        population_size, game_generator().court.width
    )

    generation_number = 0
    with tqdm(total=generation_limit) as progress_bar:
        while generation_limit is None or generation_number < generation_limit:
            parameters_list = evolve(comparator, combine, parameters_list, serialize)
            generation_number += 1
            progress_bar.update(1)
    _, evaluation = tournament(comparator, parameters_list)
    serialize(parameters_list, evaluation, True)


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
