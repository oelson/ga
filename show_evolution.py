from sys import stdout
from json import dumps as to_json

from genetic_algorithm.mutation import flip_random_bit_in_random_byte, no_mutation, Hazard
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.selection import letter_distance, bytearray_distance, bytearray_bit_distance
from genetic_algorithm.species.unicode import target_text, random_being

target = target_text('le cadavre exquis boira le vin nouveau')
mutation_probability = 1 / 5
maximum_number_of_mutations = 2
mutation_distribution = {
    no_mutation: 1 - mutation_probability,
    flip_random_bit_in_random_byte: mutation_probability,
}


def fitness(b):
    return bytearray_bit_distance(b.genotype, target.genotype)
    return bytearray_distance(b.genotype, target.genotype)
    return letter_distance(b.phenotype, target.phenotype)


def random_being_of_target_length():
    return random_being(len(target.genotype))


run = ConvergeToTarget(
    target=target,
    survival_percentile=1 / 2,
    random_being=random_being_of_target_length,
    initial_population_size=50,
    hazard=Hazard(mutation_distribution, maximum_number_of_mutations),
    fitness=fitness,
    maximum_rank=10000
)

for rank, population in run.generations():
    best = population[0]
    line = f'[{rank}] best: {best}'
    stdout.write(f'\r{line}')
