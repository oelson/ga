from sys import stdout

from genetic_algorithm.application.generations import enumerate_generations
from genetic_algorithm.mutation import no_mutation, random_byte_replacement, flit_random_bit_in_random_byte


generations = enumerate_generations(
    target_string='coucou',
    population_size=30,
    fertility_rate=2,
    mutation_distribution={
        no_mutation: 0.75,
        flit_random_bit_in_random_byte: 0.25,
    },
    maximum_rank=10000
)

for rank, population in generations:
    stdout.write(f'\r[{rank}] best: {population[0]}')
print('')
