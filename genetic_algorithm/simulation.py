from itertools import chain
from typing import Callable, List

from genetic_algorithm.mutation import Hazard
from genetic_algorithm.population import Being, Population, generate
from genetic_algorithm.selection import truncate, Fitness


class Simulation:
    def __init__(
            self,
            survival_percentile: float,
            fitness: Fitness,
            initial_being: Callable[[], Being],
            initial_population_size: int,
            hazard: Hazard,
            maximum_rank: int
    ):
        self.survival_percentile = survival_percentile
        self.fertility_rate = int(1 / survival_percentile)
        self.initial_being = initial_being
        self.initial_population_size = initial_population_size
        self.maximum_rank = maximum_rank
        self.fitness_function = fitness
        self.fitness_cache = {}
        self.hazard = hazard

    def fitness(self, b: Being):
        if b not in self.fitness_cache:
            self.fitness_cache[b] = self.fitness_function(b)
        return self.fitness_cache[b]

    def select(self, p: Population) -> Population:
        return truncate(p, self.fitness, self.survival_percentile)

    def stop(self, r: int, p: Population) -> bool:
        return r == self.maximum_rank or not p or any(self.fitness(being) == 0 for being in p)

    def life(self, b: Being, p: Population) -> Population:
        b.genotype = self.hazard(b.genotype)
        return [b.reproduce(p) for _ in range(self.fertility_rate)]

    def lifecycle(self, p: Population) -> Population:
        individual_lives = (self.life(being, p) for being in p)
        all_lives = list(chain.from_iterable(individual_lives))
        return self.select(all_lives)

    def generations(self):
        initial_population = [self.initial_being() for _ in range(self.initial_population_size)]
        return generate(initial_population, self.lifecycle, self.stop)

    def last_generation(self):
        *_, (last_rank, last_generation) = self.generations()
        return last_rank, last_generation
