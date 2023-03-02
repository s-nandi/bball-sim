from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Sequence, Optional, Tuple
from pathlib import Path
import json
from tqdm import tqdm
from ga.metadata import Metadata, TeamMetadata
from ga.evaluation import Evaluation
from ga.parameters.parameters import Parameters
from ga.parameters.regular_parameters import RegularParameters
from ga.parameters.spaced_parameters import SpacedParameters


def generation_file_name(generation_number: int):
    return f"generation_{generation_number}.json"


def generation_index(file_name: str) -> Optional[int]:
    try:
        return int(file_name.replace("generation_", "").replace(".json", ""))
    except ValueError:
        return None


def evaluations_file_name(generation_number: int):
    return f"evaluations_{generation_number}.json"


def metadata_file_name():
    return "metadata.json"


def file_name_with_index(file_name: str, index: int) -> str:
    pos = file_name.find(" (")
    if pos == -1:
        prefix = file_name
    else:
        prefix = file_name[:pos]
    return f"{prefix} ({index})"


def get_safe_path(file_path: Path) -> Path:
    safe_index = 1
    while file_path.exists():
        indexed_stem = file_name_with_index(file_path.stem, safe_index)
        file_path = file_path.with_name(indexed_stem).with_suffix(file_path.suffix)
        safe_index += 1
    return file_path


def _write_json(file_path: Path, obj, *, log=False):
    file_path = get_safe_path(file_path)
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
    folder: str
    identifier: Optional[str] = None
    serialize_gap: int = 0
    _basepath: Path = field(init=False)
    _generation_number: int = field(init=False, default=0)
    _last_serialized_generation: int = field(init=False, default=0)

    def __post_init__(self):
        if self.identifier is not None:
            print(self.identifier)
        self._basepath = (
            Path(self.folder).joinpath(self.identifier)
            if self.identifier is not None
            else Path(self.folder)
        )
        self._basepath.mkdir(exist_ok=True, parents=False)

    def _should_serialize(self):
        is_first = self._generation_number == 0
        gap = self._generation_number - self._last_serialized_generation
        always_serialize = self.serialize_gap == 0
        return is_first or gap >= self.serialize_gap or always_serialize

    def jump_to_generation(self, generation_number: int) -> ParametersSerializer:
        assert generation_number >= self._generation_number
        self._generation_number = generation_number
        return self

    def serialize_parameters(
        self, parameters_list: Sequence[Parameters], force: bool = False
    ):
        if self._should_serialize() or force:
            file_name = generation_file_name(self._generation_number)
            path = self._basepath.joinpath(file_name)
            _write_json(
                path, [asdict(parameters) for parameters in parameters_list], log=True
            )
            self._last_serialized_generation = self._generation_number
        self._generation_number += 1

    def serialize_evaluation(self, evaluations: Evaluation, force: bool = False):
        if self._should_serialize() or force:
            file_name = evaluations_file_name(self._generation_number)
            path = self._basepath.joinpath(file_name)
            _write_json(path, asdict(evaluations), log=True)

    def serialize_metadata(self, metadata: Metadata):
        file_name = metadata_file_name()
        path = self._basepath.joinpath(file_name)
        _write_json(path, asdict(metadata), log=False)


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

    def _find_max_generation_in_folder(self) -> int:
        file_names = [path.name for path in self._basepath.glob("*.json")]
        highest_generation = 0
        for file_name in file_names:
            generation_number = generation_index(file_name)
            if generation_number is None:
                continue
            highest_generation = max(highest_generation, generation_number)
        return highest_generation

    def _max_generation_that_exists_below(self, generation_number: int) -> int:
        original_number = generation_number
        while generation_number >= 0:
            file_name = generation_file_name(generation_number)
            path = self._basepath.joinpath(file_name)
            if path.exists():
                return generation_number
            generation_number -= 1
        return original_number

    def deserialize_parameters(
        self, generation_number: Optional[int]
    ) -> Tuple[int, Sequence[Parameters]]:
        if generation_number is None:
            generation_number = self._find_max_generation_in_folder()
        else:
            generation_number = self._max_generation_that_exists_below(
                generation_number
            )
        file_name = generation_file_name(generation_number)
        path = self._basepath.joinpath(file_name)
        assert isinstance(path, Path)
        parameters_objs = _read_json(path, log=True)
        parameters_list = []
        for parameters_obj in parameters_objs:
            parameters_list.append(to_parameters(parameters_obj))
        return generation_number, parameters_list

    def deserialize_metadata(self) -> Metadata:
        file_name = metadata_file_name()
        path = self._basepath.joinpath(file_name)
        json_data = _read_json(path)
        team_metadata_1 = TeamMetadata(**json_data["teams"][0])
        team_metadata_2 = TeamMetadata(**json_data["teams"][0])
        json_data.pop("teams")
        return Metadata((team_metadata_1, team_metadata_2), **json_data)
