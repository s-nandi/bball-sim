from __future__ import annotations
from typing import Callable, Tuple
from copy import deepcopy
from random import shuffle
import multiprocess as mp  # type: ignore
from ga.evaluation import Evaluation
from ga.evolution_types import IndividualComparator, IndividualCreator, Population


def rotated(lis):
    return lis[1:] + lis[:1]


DELTA = 0.1
P_CHANGE = 0.2
P_FIRST = 0.5


def tournament(
    comparator: IndividualComparator, population: Population
) -> Tuple[Population, Evaluation]:
    assert len(population) % 2 == 0
    evaluation_indices = [
        (i, j) for i in range(0, len(population)) for j in range(i + 1, len(population))
    ]
    evaluations = [(population[i], population[j]) for i, j in evaluation_indices]

    with mp.Pool(mp.cpu_count() - 2) as pool:  # pylint: disable=no-member,not-callable
        # pylint: disable=no-member
        score_differences = pool.starmap(comparator, evaluations)

    scores = [float("inf") for _ in population]
    deltas = []
    for (i, j), delta in zip(evaluation_indices, score_differences):
        scores[i] = min(scores[i], delta)
        scores[j] = min(scores[j], -delta)
        deltas.append((i, j, delta))

    indices = list(range(len(population)))
    sorted_indices = sorted(indices, key=lambda ind: scores[ind], reverse=True)
    winning_indices = sorted_indices[: len(population) // 2]

    evaluation = Evaluation(deltas, scores, winning_indices)
    return [population[ind] for ind in winning_indices], evaluation


def next_generation(creator: IndividualCreator, population: Population) -> Population:
    children = []
    for individuals_1, individuals_2 in zip(population, rotated(population)):
        child = creator(individuals_1, individuals_2, P_FIRST)
        children.append(child)
    return children


def evolve(
    comparator: IndividualComparator,
    creator: IndividualCreator,
    population: Population,
    serialize: Callable[[Population, Evaluation], None],
) -> Population:
    shuffle(population)
    if len(population) % 2 != 0:
        population.append(deepcopy(population[0]))

    winners, metrics = tournament(comparator, population)
    serialize(population, metrics)

    shuffle(winners)
    children = next_generation(creator, winners)
    population_str = (
        f"{len(population)} population,"
        f" {len(winners)} survivors,"
        f" {len(children)} children"
    )
    assert len(children) == len(winners), population_str
    assert len(children) + len(winners) == len(population), population_str
    mutated = [individual.mutate(DELTA, P_CHANGE) for individual in children]
    return mutated + list(winners)
