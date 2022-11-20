from abc import ABC, abstractmethod
from typing import Union, Iterable
import pymunk

PhysicsComponent = Union[pymunk.Shape, pymunk.Body, pymunk.Constraint]


class PhysicsObject(ABC):
    @abstractmethod
    def physics_components(self) -> Iterable[PhysicsComponent]:
        pass

    def add_to_space(self, space: pymunk.Space) -> None:
        for obj in self.physics_components():
            space.add(obj)

    def remove_from_space(self, space: pymunk.Space) -> None:
        for obj in self.physics_components():
            space.remove(obj)
