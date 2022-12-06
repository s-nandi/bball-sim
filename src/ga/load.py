from typing import Tuple, Sequence, Optional
from bball import Game
from ga.parameters import ParametersDeserializer, Parameters
from ga.metadata import Metadata
from ga.evaluation_game import evaluation_game


def load(
    folder: str, generation_number: Optional[int]
) -> Tuple[int, Game, Metadata, Sequence[Parameters]]:
    deserializer = ParametersDeserializer(folder)
    generation_number, parameters_list = deserializer.deserialize_parameters(
        generation_number
    )
    metadata = deserializer.deserialize_metadata()
    total_players = 0
    for team in metadata.teams:
        total_players += len(team.player_attributes)
    game = evaluation_game(total_players // 2)
    return generation_number, game, metadata, parameters_list
