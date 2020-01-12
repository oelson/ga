from typing import List, Callable


class Being:
    def __init__(self, genotype: bytearray, phenotype):
        self.initial_genotype = bytes(genotype)
        self.genotype = genotype
        self.phenotype = phenotype

    def __hash__(self):
        return hash(self.initial_genotype)

    def __eq__(self, other):
        return self.initial_genotype == other.initial_genotype

    def reproduce(self, population):
        return self


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
