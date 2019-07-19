from sys import stdout
from matplotlib import pyplot as plt

from genetic_algorithm.mutation import flip_random_bit_in_random_byte, no_mutation, Hazard, random_byte_replacement
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.selection import letter_distance, bytearray_distance, bytearray_bit_distance
from genetic_algorithm.species.unicode import target_text, random_being

target = target_text('le cadavre exquis boira le vin nouveau')
mutation_probability = .1
maximum_number_of_mutations = 2
mutation_distribution = {
    no_mutation: 1 - mutation_probability,
    flip_random_bit_in_random_byte: mutation_probability,
}
maximum_rank = 100000


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
    maximum_rank=maximum_rank
)

ranks = []
best_fitnesses = []
worst_fitnesses = []

for rank, population in run.generations():
    best, worst = population[0], population[-1]
    best_fitness, worst_fitness = fitness(best), fitness(worst)
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
