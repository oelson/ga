from sys import stdout
from matplotlib import pyplot as plt

from genetic_algorithm import mutation
from genetic_algorithm.scenario.converge import Converge
from genetic_algorithm.species.unicode import TextTarget, clone_being

target = TextTarget('le cadavre exquis boira le vin nouveau')

run = Converge(
    survival_percentile=1 / 2,
    initial_being=target.random_being,
    initial_population_size=100,
    reproduce_being=clone_being,
    hazard=mutation.build_hazard(
        mutation_probability=1 / 10,
        mutation_distribution={
            mutation.flip_random_bit_in_random_byte: 1 / 2,
            mutation.random_byte_replacement: 1 / 2
        },
        maximum_number_of_mutations=2),
    fitness=target.fitness_by_genotype,
    maximum_rank=10000
)

ranks = []
best_fitnesses = []
worst_fitnesses = []

for rank, population in run.generations():
    best, worst = population[0], population[-1]
    best_fitness, worst_fitness = run.fitness(best), run.fitness(worst)
    ranks.append(rank)
    best_fitnesses.append(best_fitness)
    worst_fitnesses.append(worst_fitness)
    stdout.write((f'\r[{rank}] '
                  f'fitness:{best_fitness}-{worst_fitness} '
                  f'best: {{genotype:{best.genotype.hex()}, phenotype:{repr(best.phenotype)}}}'))

max_fitness = max(best_fitnesses)
min_fitness = 0

fig, ax = plt.subplots()
ax.plot(ranks, worst_fitnesses, label='worst')
ax.plot(ranks, best_fitnesses, label='best')
ax.set(xlabel='rank', ylabel='fitness')
ax.set_ylim(min_fitness, max_fitness)
ax.legend()
ax.margins(x=0, y=0)
plt.show()
