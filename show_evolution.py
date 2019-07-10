from sys import stdout

from genetic_algorithm.mutation import no_mutation, random_byte_replacement, flit_random_bit_in_random_byte

from genetic_algorithm.selection import bytearray_distance, truncate
from genetic_algorithm.population import generate, select_over_all_livings
from genetic_algorithm.scenario.unicode import Being, Population, target_being, random_being, mutate_and_clone


def fitness(b: Being):
    return bytearray_distance(b.genotype, target.genotype)


def select(p: Population):
    return truncate(p, fitness, survival_percentile)


def stop(r: int, p: Population) -> bool:
    return r == maximum_rank or not population or any(fitness(being) == 0 for being in p)


def life(b: Being):
    return mutate_and_clone(b, mutation_distribution, fertility_rate)


def lifecycle(p: Population) -> Population:
    return select_over_all_livings(p, life, select)


target = target_being('le cadavre exquis boira le vin nouveau')
mutation_probability = .25
mutation_function = random_byte_replacement
fertility_rate = 2
survival_percentile = 1 / fertility_rate
initial_population_size = 30
initial_population = [random_being(len(target.genotype)) for _ in range(initial_population_size)]
mutation_distribution = {
    no_mutation: 1 - mutation_probability,
    mutation_function: mutation_probability,
}
maximum_rank = 10000

for rank, population in generate(initial_population, lifecycle, stop):
    stdout.write(f'\r[{rank}] best: {population[0]}')
