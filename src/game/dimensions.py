import dataclasses
from typing import Tuple


@dataclasses.dataclass
class RimDimensions:
    radius: float
    distance_from_left_edge: float


@dataclasses.dataclass
class ThreePointLineDimensions:
    distance_from_top_edge: float
    corner_length: float
    outer_radius: float
    line_thickness: float


@dataclasses.dataclass
class CourtDimensions:
    width: float
    height: float
    boundary_thickness: float
    rim: RimDimensions
    three_point_line: ThreePointLineDimensions
    boundary_thickness_diameter: float = dataclasses.field(init=False)

    def __post_init__(self):
        self.boundary_thickness_diameter = self.boundary_thickness * 1

    @property
    def x_min(self) -> float:
        return self.boundary_thickness_diameter

    @property
    def x_max(self) -> float:
        return self.width - self.boundary_thickness_diameter

    @property
    def x_mid(self) -> float:
        return (self.x_min + self.x_max) / 2

    @property
    def y_min(self) -> float:
        return self.boundary_thickness_diameter

    @property
    def y_max(self) -> float:
        return self.height - self.boundary_thickness_diameter

    @property
    def y_mid(self) -> float:
        return (self.y_min + self.y_max) / 2

    @property
    def left_rim_position(self) -> Tuple[float, float]:
        return (
            self.x_min + self.rim.distance_from_left_edge,
            self.y_mid,
        )

    @property
    def right_rim_position(self) -> Tuple[float, float]:
        return (
            self.x_max - self.rim.distance_from_left_edge,
            self.y_mid,
        )
