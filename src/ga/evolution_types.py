from __future__ import annotations
from typing import MutableSequence, Callable, Protocol, TypeVar

T = TypeVar("T")


class IndividualInterface(Protocol):
    type: str

    def mutate(self: T, delta: float, p_change: float) -> T:
        pass

    def crossover(self: T, other: T, p_first: float) -> T:
        pass


Individual = TypeVar("Individual")
IndividualComparator = Callable[[Individual, Individual], float]
IndividualCreator = Callable[[Individual, Individual, float], Individual]
Population = MutableSequence[IndividualInterface]
