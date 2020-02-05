from sys import stdout
from matplotlib import pyplot as plt

from genetic_algorithm import mutation
from genetic_algorithm.simulation import Simulation
from genetic_algorithm.species.text import TextTarget
from genetic_algorithm.presentation import byte_string

target = TextTarget('le cadavre exquis boira le vin nouveau', 'ascii')

run = Simulation(
    survival_percentile=1 / 8,
    initial_being=target.random_being,
    initial_population_size=30,
    maximum_rank=10000,

    hazard=mutation.Hazard.build(
        mutation_probability=1 / 2,
        mutation_distribution={
            mutation.replace_random_letter(target.alphabet()): 0,
            mutation.replace_random_byte: .5,
            mutation.replace_random_bit: .5,
        },
        maximum_number_of_mutations=1),

    fitness=target.fitness_by_phenotype,
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
                  f'best: {{genotype:{byte_string(best.genotype)}, phenotype:{repr(best.phenotype)}}}'))

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