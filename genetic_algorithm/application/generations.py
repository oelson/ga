from genetic_algorithm.selection import truncate, bytearray_bit_distance, bytearray_distance, letter_distance
from genetic_algorithm.population import generate, select_over_all_livings, any_perfect_being_in_population
from genetic_algorithm.scenario.unicode import Being, Population, random_population, target_being, being_lifecycle


def enumerate_generations(
        target_string: str,
        population_size: int,
        fertility_rate: int,
        mutation_distribution: dict,
        maximum_rank: int) -> callable:
    target = target_being(target_string)
    survival_percentile = 1 / fertility_rate

    def initial_population() -> Population:
        return random_population(population_size, len(target.genotype))

    def fitness(being: Being) -> float:
        return letter_distance(being.phenotype, target.phenotype)
        return bytearray_distance(being.genotype, target.genotype)

    def stop(rank: int, population: Population) -> bool:
        return rank == maximum_rank or any_perfect_being_in_population(population, fitness)

    def lifecycle(population: Population) -> Population:
        return select_over_all_livings(
            population,
            lambda b: being_lifecycle(b, mutation_distribution, fertility_rate),
            lambda p: truncate(p, fitness, survival_percentile))

    return generate(initial_population(), lifecycle, stop)