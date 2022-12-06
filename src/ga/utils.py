from __future__ import annotations
from typing import TypeVar
from random import uniform, random


def crossover(val1, val2, p_first: float):
    if random() < p_first:
        return val1
    return val2


T = TypeVar("T", float, bool)


def mutate(val: T, delta: T, prob: float):
    if random() < prob:
        if isinstance(val, float):
            return val + uniform(-delta, delta)
        if isinstance(val, bool):
            return val ^ delta
        assert False
    else:
        return val
