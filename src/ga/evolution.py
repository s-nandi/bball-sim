from __future__ import annotations
from copy import deepcopy
from typing import List, Callable, TypeVar
from random import shuffle


def rotated(lis):
    return lis[1:] + lis[:1]


DELTA = 0.1
P_CHANGE = 0.1
P_FIRST = 0.5

Individual = TypeVar("Individual")
IndividualComparator = Callable[[Individual, Individual], bool]
IndividualCreator = Callable[[Individual, Individual, float], Individual]
Population = List[Individual]


def tournament(comparator: IndividualComparator, population: Population) -> Population:
    if len(population) % 2 != 0:
        population.append(deepcopy(population[0]))
    shuffle(population)
    winners = []
    for i in range(0, len(population), 2):
        individual_1 = population[i]
        individual_2 = population[i + 1]
        winner_is_1 = comparator(individual_1, individual_2)
        if winner_is_1:
            winners.append(individual_1)
        else:
            winners.append(individual_2)
    return winners


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
