from typing import List, Callable
from itertools import chain


class Being:
    def __init__(self, genotype: bytearray, phenotype):
        self.initial_genotype = bytes(genotype)
        self.genotype = genotype
        self.phenotype = phenotype

    def reproduce(self, population):
        pass

    def to_dict(self):
        return {
            'phenotype': self.phenotype,
            'genotype': self.genotype.hex()
        }

    def __hash__(self):
        return hash(self.initial_genotype)

    def __eq__(self, other):
        return self.initial_genotype == other.initial_genotype


Population = List[Being]

Life = Callable[[Being, Population], Population]

Cycle = Callable[[Population], Population]

Selection = Callable[[Population], Population]

StopGeneration = Callable[[int, Population], bool]


def generate(initial_population: Population, lifecycle: Cycle, stop: StopGeneration):
    rank, population = 1, initial_population

    while not stop(rank, population):
        yield rank, population
        rank, population = rank + 1, lifecycle(population)


def select_over_all_livings(population: Population, life: Life, selection: Selection) -> Population:
    lives = (life(being, population) for being in population)
    all_lives = list(chain.from_iterable(lives))
    return selection(all_lives)
