from typing import Callable

from genetic_algorithm.mutation import Hazard
from genetic_algorithm.selection import bytearray_bit_distance, letter_distance, truncate, Fitness, EfficientFitness
from genetic_algorithm.population import Being, Population, generate, select_over_all_livings


class ConvergeToTarget:
    def __init__(
            self,
            survival_percentile: float,
            fitness: Fitness,
            random_being: Callable[[], Being],
            initial_population_size: int,
            hazard: Hazard,
            maximum_rank: int
    ):
        self.survival_percentile = survival_percentile
        self.fertility_rate = int(1 / survival_percentile)
        self.random_being = random_being
        self.initial_population_size = initial_population_size
        self.maximum_rank = maximum_rank
        self._fitness = fitness
        self.fitness = EfficientFitness(fitness)
        self.hazard = hazard

    def select(self, p: Population) -> Population:
        return truncate(p, self.fitness, self.survival_percentile)

    def stop(self, r: int, p: Population) -> bool:
        return r == self.maximum_rank or not p or any(self.fitness(being) == 0 for being in p)

    def life(self, b: Being, p: Population) -> Population:
        b.genotype = self.hazard(b.genotype)
        return [b.reproduce(p) for _ in range(self.fertility_rate)]

    def lifecycle(self, p: Population) -> Population:
        return select_over_all_livings(p, self.life, self.select)

    def generations(self):
        return generate(
            [self.random_being() for _ in range(self.initial_population_size)],
            self.lifecycle,
            self.stop)

    def last_generation(self):
        *_, (last_rank, last_generation) = self.generations()
        return last_rank, last_generation
