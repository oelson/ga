from sys import stdout

from genetic_algorithm.mutation import no_mutation, random_byte_replacement, flit_random_bit_in_random_byte

from genetic_algorithm.selection import bytearray_distance, bytearray_bit_distance, letter_distance, truncate
from genetic_algorithm.population import generate, select_over_all_livings
from genetic_algorithm.scenario.unicode import Being, Population, target_being, random_being, mutate_and_clone


def initial_population() -> Population:
    return [random_being(len(target.genotype)) for _ in range(initial_population_size)]


def fitness(b: Being):
    return letter_distance(b.phenotype, target.phenotype)
    return bytearray_bit_distance(b.genotype, target.genotype)
    return bytearray_distance(b.genotype, target.genotype)


def select(p: Population):
    return truncate(p, fitness, survival_percentile)


def stop(r: int, p: Population) -> bool:
    return r == maximum_rank or not p or any(fitness(being) == 0 for being in p)


def life(b: Being):
    return mutate_and_clone(b, maximum_number_of_mutations, mutation_distribution, fertility_rate)


def lifecycle(p: Population) -> Population:
    return select_over_all_livings(p, life, select)


target = target_being('le cadavre exquis boira le vin nouveau')
maximum_number_of_mutations = 2
mutation_probability = 1 / 5
mutation_function = flit_random_bit_in_random_byte
survival_percentile = 1 / 2
fertility_rate = int(1 / survival_percentile)
initial_population_size = 100
mutation_distribution = {
    no_mutation: 1 - mutation_probability,
    mutation_function: mutation_probability,
}
maximum_rank = 50000

for rank, population in generate(initial_population(), lifecycle, stop):
    line = f'[{rank}] best: {population[0]}'
    # print(line)
    stdout.write(f'\r{line}')
