from sys import stdout
from matplotlib import pyplot as plt

from genetic_algorithm.mutation import flip_random_bit_in_random_byte, no_mutation, Hazard, random_byte_replacement
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.species.unicode import TextTarget

target = TextTarget('le cadavre exquis boira le vin nouveau')
mutation_probability = .1
maximum_number_of_mutations = 2
mutation_distribution = {
    no_mutation: 1 - mutation_probability,
    flip_random_bit_in_random_byte: mutation_probability,
}
maximum_rank = 100000
survival_percentile = .5
initial_population_size = 100

run = ConvergeToTarget(
    survival_percentile=survival_percentile,
    random_being=target.random_being,
    initial_population_size=initial_population_size,
    hazard=Hazard(mutation_distribution, maximum_number_of_mutations),
    fitness=target.fitness_by_genotype,
    maximum_rank=maximum_rank
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
                  f'best: {{phenotype:{repr(best.phenotype)}, genotype:{best.genotype.hex()}}}'))

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
