from typing import List, Callable
from binascii import hexlify
from itertools import chain


class Being:
    def __init__(self, genotype: bytearray, phenotype):
        self.genotype = genotype
        self.phenotype = phenotype

    def reproduce(self, population):
        pass

    def __str__(self):
        return f'{{phenotype:{repr(self.phenotype)}, genotype:{hexlify(self.genotype)}}}'

    def __repr__(self):
        return self.__str__()


Population = List[Being]

Life = Callable[[Being, Population], Population]

Cycle = Callable[[Population], Population]

Selection = Callable[[Population], Population]

StopGeneration = Callable[[int, Population], bool]


def generate(initial_population: Population, lifecycle: Cycle, stop: StopGeneration):
    rank, population = 1, initial_population
    yield rank, population

    while not stop(rank, population):
        rank, population = rank + 1, lifecycle(population)
        yield rank, population


def select_over_all_livings(population: Population, life: Life, selection: Selection) -> Population:
    lives = (life(being, population) for being in population)
    all_lives = list(chain.from_iterable(lives))
    return selection(all_lives)
