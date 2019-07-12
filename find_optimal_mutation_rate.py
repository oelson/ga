from numpy import mean
from itertools import product

from genetic_algorithm.mutation import no_mutation, flit_random_bit_in_random_byte
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.selection import letter_distance, bytearray_distance
from genetic_algorithm.species.unicode import target_text, random_being


def measure(run: ConvergeToTarget):
    generations = run.generations()
    *_, (last_rank, last_generation) = generations
    asymptotic_fitness = float(mean([run.fitness(being) for being in last_generation]))
    return last_rank, asymptotic_fitness, last_generation[0]


def average(configuration, number_of_runs):
    runs = [ConvergeToTarget(**configuration) for _ in range(number_of_runs)]
    measures = [measure(run) for run in runs]

    average_asymptotic_fitness = float(mean([f for f, _, _ in measures]))
    average_maximal_rank = float(mean([r for _, r, _ in measures]))
    sample_being = next(b for _, _, b in measures)

    return average_asymptotic_fitness, average_maximal_rank, sample_being


target = target_text('cadavre')


def fitness_by_phenotype(b):
    return letter_distance(b.phenotype, target.phenotype)


def fitness_by_genotype(b):
    return bytearray_distance(b.genotype, target.genotype)


mutation_function = flit_random_bit_in_random_byte
number_of_runs_per_simulation = 3

mutation_probability_space = [.9, .5, .1]
maximum_number_of_mutations_space = [1, 2, 3, 4]
initial_population_size_space = [20, 50]
survival_percentile_space = [1 / 2, 1 / 3, 1 / 4]
fitness_function_space = [fitness_by_phenotype, fitness_by_genotype]

configuration_space = product(
    maximum_number_of_mutations_space,
    mutation_probability_space,
    survival_percentile_space,
    initial_population_size_space,
    fitness_function_space
)

for (
        maximum_number_of_mutations,
        mutation_probability,
        survival_percentile,
        initial_population_size,
        fitness_function
) in configuration_space:
    configuration = {
        'target': target,
        'initial_population': [random_being(len(target.genotype)) for _ in range(initial_population_size)],
        'survival_percentile': survival_percentile,
        'maximum_number_of_mutations': maximum_number_of_mutations,
        'mutation_distribution': {
            no_mutation: 1 - mutation_probability,
            mutation_function: mutation_probability,
        },
        'fitness': fitness_function,
        'maximum_rank': 1000
    }

    print((
        f'maximum number of mutations: {maximum_number_of_mutations}, '
        f'mutation probability: {mutation_probability:.02f}, '
        f'fitness function: {fitness_function.__name__}, '
        f'survival percentile: {survival_percentile:.02f}, '
        f'initial population size: {initial_population_size}'
    ))

    average_maximal_rank, asymptotic_fitness, sample_being = average(configuration, number_of_runs_per_simulation)

    print(f'\taverage maximal rank: {average_maximal_rank:.02f}')
    print(f'\tasymptotic fitness: {asymptotic_fitness:.02f}')
    print(f'\tsample being: {sample_being}')
