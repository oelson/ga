from genetic_algorithm.mutation import no_mutation
from genetic_algorithm.selection import bytearray_bit_distance, truncate
from genetic_algorithm.population import Being, Population, generate, select_over_all_livings
from genetic_algorithm.species.unicode import target_being, random_being, mutate_and_clone


class ConvergeToTarget:
    def __init__(
            self,
            target_string,
            survival_percentile,
            initial_population_size,
            maximum_number_of_mutations,
            mutation_distribution,
            maximum_rank
    ):
        self.target = target_being(target_string)
        self.survival_percentile = survival_percentile
        self.fertility_rate = int(1 / survival_percentile)
        self.initial_population_size = initial_population_size
        self.maximum_number_of_mutations = maximum_number_of_mutations
        self.mutation_distribution = mutation_distribution
        self.maximum_rank = maximum_rank

    def initial_population(self) -> Population:
        return [random_being(len(self.target.genotype)) for _ in range(self.initial_population_size)]

    def fitness(self, b: Being) -> float:
        return bytearray_bit_distance(b.genotype, self.target.genotype)

    def select(self, p: Population) -> Population:
        return truncate(p, self.fitness, self.survival_percentile)

    def stop(self, r: int, p: Population) -> bool:
        return r == self.maximum_rank or not p or any(self.fitness(being) == 0 for being in p)

    def life(self, b: Being) -> Population:
        return mutate_and_clone(b, self.maximum_number_of_mutations, self.mutation_distribution, self.fertility_rate)

    def lifecycle(self, p: Population) -> Population:
        return select_over_all_livings(p, self.life, self.select)

    def generations(self):
        return generate(self.initial_population(), self.lifecycle, self.stop)
