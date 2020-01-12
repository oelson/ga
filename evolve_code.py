from sys import stdout
from typing import Sequence

from genetic_algorithm.mutation import replace_random_bit, Hazard
from genetic_algorithm.simulation import Simulation
from genetic_algorithm.species.python_code import source_code_to_bytecode, PythonBeing, clone_being

'''
trouver un moyen de gérer les progénitures malformées:
comment préserver la taille de la population si tous les individus engendrent des malformés ?
même pas un seul reproducteur...
'''

prototype_bytecode = source_code_to_bytecode('''
for i in range(1, len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] < numbers[j]:
            numbers[i], numbers[j] = numbers[j], numbers[i]
''', '/Users/nelson/Desktop/PYCOMPILE')


def count_sorted(unsorted_list: Sequence[int]) -> int:
    if unsorted_list is None:
        return 1000
    sorted_list = sorted(unsorted_list)
    return sum(1 for n, m in zip(unsorted_list, sorted_list) if n != m)


run = Simulation(
    survival_percentile=1 / 2,
    initial_being=lambda: PythonBeing(bytearray(prototype_bytecode)),
    initial_population_size=100,
    reproduce_being=clone_being,
    hazard=Hazard.build(
        mutation_probability=1 / 10,
        mutation_distribution={replace_random_bit: 1},
        maximum_number_of_mutations=2),
    fitness=lambda b: count_sorted(b.phenotype),
    maximum_rank=10000
)

for rank, population in run.generations():
    best, worst = population[0], population[-1]
    best_fitness, worst_fitness = run.fitness(best), run.fitness(worst)
    stdout.write(
        (f'\r[{rank}] '
         f'fitness:{best_fitness}-{worst_fitness} '
         f'best: {{phenotype:{repr(best.phenotype)}, genotype:{best.genotype.hex()}}}'))
