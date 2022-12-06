from dataclasses import dataclass, asdict, field
from typing import Sequence
from pathlib import Path
import json
from tqdm import tqdm
from ga.metadata import Metadata
from ga.parameters.parameters import Parameters
from ga.parameters.regular_parameters import RegularParameters
from ga.parameters.spaced_parameters import SpacedParameters


def generation_file_name(generation_number: int):
    return f"generation_{generation_number}.json"


def metadata_file_name():
    return "metadata.json"


def _write_json(file_path: Path, obj, *, log=False):
    if log:
        tqdm.write(f"writing {file_path}")
    json_obj = json.dumps(obj)
    with open(file_path, "w", encoding="utf-8") as output_file:
        output_file.write(json_obj)


def _read_json(file_path: Path, *, log=False):
    if log:
        tqdm.write(f"reading {file_path}")
    with open(file_path, "r", encoding="utf-8") as input_file:
        return json.load(input_file)


@dataclass
class ParametersSerializer:
    identifier: str
    folder: str
    serialize_frequency: int
    _basepath: Path = field(init=False)
    _generation_number: int = field(init=False, default=0)
    _last_serialized_generation: int = field(init=False, default=0)

    def __post_init__(self):
        self._basepath = Path(self.folder).joinpath(self.identifier)
        self._basepath.mkdir(exist_ok=False, parents=False)

    def serialize_parameters(
        self, parameters_list: Sequence[Parameters], force: bool = False
    ):
        is_first = self._generation_number == 0
        gap = self._generation_number - self._last_serialized_generation
        should_serialize = force or is_first or gap >= self.serialize_frequency
        if should_serialize:
            file_name = generation_file_name(self._generation_number)
            path = self._basepath.joinpath(file_name)
            _write_json(
                path, [asdict(parameters) for parameters in parameters_list], log=True
            )
            self._last_serialized_generation = self._generation_number
        self._generation_number += 1

    def serialize_metadata(self, metadata: Metadata):
        file_name = metadata_file_name()
        path = self._basepath.joinpath(file_name)
        _write_json(path, asdict(metadata), log=True)


def to_parameters(obj) -> Parameters:
    parameters_type = obj.pop("type")
    if parameters_type == "regular":
        return RegularParameters(**obj)
    if parameters_type == "spaced":
        return SpacedParameters(**obj)
    error_msg = f"invalid {parameters_type} parameter, must be regular or spaced"
    assert False, error_msg


@dataclass
class ParametersDeserializer:
    folder: str
    _basepath: Path = field(init=False)

    def __post_init__(self):
        self._basepath = Path(self.folder)
        assert self._basepath.is_dir()

    def _max_generation_that_exists_below(self, generation_number: int) -> int:
        original_number = generation_number
        while generation_number >= 0:
            file_name = generation_file_name(generation_number)
            path = self._basepath.joinpath(file_name)
            if path.exists():
                return generation_number
            generation_number -= 1
        return original_number

    def deserialize_parameters(self, generation_number: int) -> Sequence[Parameters]:
        generation_number = self._max_generation_that_exists_below(generation_number)
        file_name = generation_file_name(generation_number)
        path = self._basepath.joinpath(file_name)
        assert isinstance(path, Path)
        parameters_objs = _read_json(path, log=True)
        parameters_list = []
        for parameters_obj in parameters_objs:
            parameters_list.append(to_parameters(parameters_obj))
        return parameters_list

    def deserialize_metadata(self) -> Metadata:
        file_name = metadata_file_name()
        path = self._basepath.joinpath(file_name)
        return Metadata(**_read_json(path))
