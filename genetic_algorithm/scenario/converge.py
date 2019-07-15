from genetic_algorithm.mutation import mutate_being
from genetic_algorithm.selection import bytearray_bit_distance, letter_distance, truncate, Fitness, EfficientFitness
from genetic_algorithm.population import Being, Population, generate, select_over_all_livings


class ConvergeToTarget:
    def __init__(
            self,
            target: Being,
            survival_percentile: float,
            fitness: Fitness,
            initial_population: Population,
            maximum_number_of_mutations: int,
            mutation_distribution: dict,
            maximum_rank: int
    ):
        self.target = target
        self.survival_percentile = survival_percentile
        self.fertility_rate = int(1 / survival_percentile)
        self.initial_population = initial_population
        self.maximum_number_of_mutations = maximum_number_of_mutations
        self.mutation_distribution = mutation_distribution
        self.maximum_rank = maximum_rank
        self.fitness = EfficientFitness(fitness)

    def select(self, p: Population) -> Population:
        return truncate(p, self.fitness, self.survival_percentile)

    def stop(self, r: int, p: Population) -> bool:
        return r == self.maximum_rank or not p or any(self.fitness(being) == 0 for being in p)

    def life(self, b: Being, p: Population) -> Population:
        b = mutate_being(b, self.maximum_number_of_mutations, self.mutation_distribution)
        return [b.reproduce(p) for _ in range(self.fertility_rate)]

    def lifecycle(self, p: Population) -> Population:
        return select_over_all_livings(p, self.life, self.select)

    def generations(self):
        return generate(self.initial_population, self.lifecycle, self.stop)

    def last_generation(self):
        *_, (last_rank, last_generation) = self.generations()
        return last_rank, last_generation
