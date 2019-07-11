from sys import stdout

from genetic_algorithm.mutation import flit_random_bit_in_random_byte, no_mutation
from genetic_algorithm.scenario.converge import ConvergeToTarget

mutation_probability = 1 / 5

convergence = ConvergeToTarget(
    target_string='le cadavre exquis boira le vin nouveau',
    survival_percentile=1 / 2,
    initial_population_size=50,
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
