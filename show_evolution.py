from sys import stdout

from genetic_algorithm.mutation import flit_random_bit_in_random_byte, no_mutation
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.selection import letter_distance, letter_distance_diff, bytearray_distance, bytearray_bit_distance
from genetic_algorithm.species.unicode import target_text, random_being

mutation_probability = 1 / 5
target = target_text('le cadavre exquis boira le vin nouveau')


def fitness_by_genotype(b):
    return bytearray_bit_distance(b.genotype, target.genotype)
    return bytearray_distance(b.genotype, target.genotype)


def fitness_by_phenotype(b):
    return letter_distance_diff(b.phenotype, target.phenotype)
    return letter_distance(b.phenotype, target.phenotype)


def random_being_of_target_length():
    return random_being(len(target.genotype))


run = ConvergeToTarget(
    target=target,
    survival_percentile=1 / 2,
    random_being=random_being_of_target_length,
    initial_population_size=50,
    maximum_number_of_mutations=2,
    mutation_distribution={
        no_mutation: 1 - mutation_probability,
        flit_random_bit_in_random_byte: mutation_probability,
    },
    fitness=fitness_by_genotype,
    maximum_rank=10000
)

for rank, population in run.generations():
    line = f'[{rank}] best: {population[0]}'
    stdout.write(f'\r{line}')
