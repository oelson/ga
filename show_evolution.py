from sys import stdout

from genetic_algorithm.mutation import flit_random_bit_in_random_byte, no_mutation
from genetic_algorithm.scenario.converge import RandomToTarget
from genetic_algorithm.species.unicode import target_text, random_being

mutation_probability = 1 / 5
target = target_text('le cadavre exquis boira le vin nouveau')

convergence = RandomToTarget(
    target=target,
    survival_percentile=1 / 2,
    initial_population=[random_being(len(target.genotype)) for _ in range(50)],
    maximum_number_of_mutations=2,
    mutation_distribution={
        no_mutation: 1 - mutation_probability,
        flit_random_bit_in_random_byte: mutation_probability,
    },
    maximum_rank=1000
)

for rank, population in convergence.generations():
    line = f'[{rank}] best: {population[0]}'
    # print(line)
    stdout.write(f'\r{line}')
