from __future__ import annotations
from typing import Callable, Tuple, Dict, List
from copy import copy
from random import shuffle
import multiprocess as mp  # type: ignore
from ga.evaluation import Evaluation
from ga.evolution_types import (
    IndividualComparator,
    IndividualCreator,
    Population,
    IndividualInterface,
)


def rotated(lis):
    return lis[1:] + lis[:1]


DELTA = 0.1
P_CHANGE = 0.4
P_FIRST = 0.5
PRESERVE_TYPE_RATIOS = True


def determine_winning_indices(sorted_indices: List[int], types: List[str]) -> List[int]:
    assert len(sorted_indices) % 2 == 0
    if not PRESERVE_TYPE_RATIOS:
        return sorted_indices[: len(sorted_indices) // 2]

    type_counts = {index_type: 0 for index_type in types}
    winner_counts = copy(type_counts)
    for index_type in types:
        type_counts[index_type] += 1

    extra = len(sorted_indices) // 2
    min_reduction = extra // len(type_counts)
    num_one_more_reduction = extra - len(type_counts) * min_reduction
    for key in type_counts:
        reduction = min_reduction
        if num_one_more_reduction > 0:
            reduction += 1
            num_one_more_reduction -= 1
        type_counts[key] -= reduction

    winner_indices = []
    for index, index_type in zip(sorted_indices, types):
        if winner_counts[index_type] < type_counts[index_type]:
            winner_indices.append(index)
            winner_counts[index_type] += 1
    return winner_indices


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

    sorted_indices = sorted(
        list(range(len(population))), key=lambda ind: scores[ind], reverse=True
    )
    types = [population[index].type for index in sorted_indices]
    winning_indices = determine_winning_indices(sorted_indices, types)

    evaluation = Evaluation(deltas, scores, winning_indices)
    return [population[ind] for ind in winning_indices], evaluation


def next_generation(creator: IndividualCreator, population: Population) -> Population:
    if not PRESERVE_TYPE_RATIOS:
        groups = [population]
    else:
        groups_dict: Dict[str, List[IndividualInterface]] = {
            individual.type: [] for individual in population
        }
        for individual in population:
            groups_dict[individual.type].append(individual)
        groups = list(groups_dict.values())

    children = []
    for group in groups:
        for individuals_1, individuals_2 in zip(group, rotated(group)):
            child = creator(individuals_1, individuals_2, P_FIRST)
            children.append(child)
    return children


def group_signature(population: Population) -> Dict[str, int]:
    sig = {individual.type: 0 for individual in population}
    for individual in population:
        sig[individual.type] += 1
    return sig


def check_population_type(old_population: Population, new_population: Population):
    if PRESERVE_TYPE_RATIOS:
        old_signature = group_signature(old_population)
        new_signature = group_signature(new_population)
        signature_str = f"expected: {old_signature} got: {new_signature}"
        assert old_signature == new_signature, signature_str


def evolve(
    comparator: IndividualComparator,
    creator: IndividualCreator,
    population: Population,
    serialize: Callable[[Population, Evaluation], None],
) -> Population:
    shuffle(population)
    assert len(population) % 2 == 0
    winners, metrics = tournament(comparator, population)
    serialize(population, metrics)

    shuffle(winners)
    children = next_generation(creator, winners)
    check_population_type(winners, children)

    population_str = (
        f"{len(population)} population,"
        f" {len(winners)} survivors,"
        f" {len(children)} children"
    )
    assert len(children) + len(winners) == len(population), population_str
    mutated = [individual.mutate(DELTA, P_CHANGE) for individual in children]
    next_population = mutated + list(winners)
    check_population_type(population, next_population)
    return next_population
