from __future__ import annotations
from typing import List, Callable, TypeVar
from copy import deepcopy
from random import shuffle
import multiprocess as mp  # type: ignore


def rotated(lis):
    return lis[1:] + lis[:1]


DELTA = 0.1
P_CHANGE = 0.2
P_FIRST = 0.5

Individual = TypeVar("Individual")
IndividualComparator = Callable[[Individual, Individual], float]
IndividualCreator = Callable[[Individual, Individual, float], Individual]
Population = List[Individual]


def tournament(comparator: IndividualComparator, population: Population) -> Population:
    if len(population) % 2 != 0:
        population.append(deepcopy(population[0]))
    shuffle(population)

    evaluation_indices = [
        (i, j) for i in range(0, len(population)) for j in range(i + 1, len(population))
    ]
    evaluations = []
    for i, j in evaluation_indices:
        evaluations = [(population[i], population[j])]

    with mp.Pool(mp.cpu_count() - 2) as pool:  # pylint: disable=no-member,not-callable
        deltas = pool.starmap(comparator, evaluations)  # pylint: disable=no-member

    scores = [float("inf") for _ in population]
    for (i, j), deltas in zip(evaluation_indices, deltas):
        scores[i] = min(scores[i], -deltas)
        scores[j] = min(scores[j], deltas)

    indices = [i for _ in population]
    winning_indices = sorted(indices, key=lambda ind: scores[ind], reverse=True)
    half_length = len(population) // 2
    return [population[ind] for ind in winning_indices[:half_length]]


def next_generation(creator: IndividualCreator, population: Population) -> Population:
    shuffle(population)
    children = []
    for parameters_1, parameters_2 in zip(population, rotated(population)):
        child = creator(parameters_1, parameters_2, P_FIRST)
        children.append(child)
    return population + children


def evolve(
    comparator: IndividualComparator, creator: IndividualCreator, population: Population
) -> Population:
    winners = tournament(comparator, population)
    shuffle(winners)
    new_population = next_generation(creator, winners)
    population_str = (
        f"{len(population)} population,"
        f" {len(winners)} survivors,"
        f" {len(new_population)} new population"
    )
    assert len(new_population) == len(population), population_str
    mutated = [parameters.mutate(DELTA, P_CHANGE) for parameters in new_population]
    return mutated
