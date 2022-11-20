import dataclasses


@dataclasses.dataclass
class CourtDimensions:
    width: float
    height: float
    boundary_thickness: float
    rim_radius: float
    rim_distance_from_edge: float
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
