from typing import Tuple, Sequence
from bball import Game
from ga.parameters import ParametersDeserializer, Parameters
from ga.evaluation_game import evaluation_game


def load(folder: str, generation_number: int) -> Tuple[Game, Sequence[Parameters]]:
    deserializer = ParametersDeserializer(folder)
    parameters_list = deserializer.deserialize_parameters(generation_number)
    metadata = deserializer.deserialize_metadata()

    total_players = 0
    for team in metadata.teams:
        total_players += len(team)
    game = evaluation_game(total_players // 2)
    return game, parameters_list
