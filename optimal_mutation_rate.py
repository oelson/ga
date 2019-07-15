from statistics import mean
from itertools import product

from genetic_algorithm.mutation import Hazard, no_mutation, flip_random_bit_in_random_byte, random_byte_replacement, \
    Mutation
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.selection import letter_distance, bytearray_distance, Fitness
from genetic_algorithm.population import Being
from genetic_algorithm.species.unicode import target_text, random_being

target = target_text('cadavre')
number_of_runs_per_simulation = 3
maximum_rank = 1000
mutation_function_space = [flip_random_bit_in_random_byte, random_byte_replacement]
mutation_probability_space = [.9, .5, .1]
maximum_number_of_mutations_space = [1, 2, 3, 4]
initial_population_size_space = [20, 50]
survival_percentile_space = [1 / 2, 1 / 3, 1 / 4]


def fitness_by_phenotype(b):
    return letter_distance(b.phenotype, target.phenotype)


def fitness_by_genotype(b):
    return bytearray_distance(b.genotype, target.genotype)


fitness_function_space = [fitness_by_phenotype, fitness_by_genotype]


def configure(
        mutation_function: Mutation,
        maximum_number_of_mutations: int,
        mutation_probability: float,
        survival_percentile: float,
        initial_population_size: int,
        fitness_function: Fitness
):
    mutation_distribution = {
        no_mutation: 1 - mutation_probability,
        mutation_function: mutation_probability,
    }
    return ConvergeToTarget(
        target=target,
        random_being=random_being_of_target_length,
        initial_population_size=initial_population_size,
        survival_percentile=survival_percentile,
        hazard=Hazard(mutation_distribution, maximum_number_of_mutations),
        fitness=fitness_function,
        maximum_rank=maximum_rank
    )


def asymptotic_average_fitness(run: ConvergeToTarget, number_of_runs: int) -> (float, float, Being):
    measures = [last_generation_fitness(run) for _ in range(number_of_runs)]

    average_asymptotic_fitness = mean(f for f, _, _ in measures)
    average_maximal_rank = mean(r for _, r, _ in measures)
    sample_being = next(b for _, _, b in measures)

    return average_asymptotic_fitness, average_maximal_rank, sample_being


def last_generation_fitness(run: ConvergeToTarget) -> (int, float, Being):
    last_rank, last_generation = run.last_generation()
    mean_fitness = mean(run.fitness(being) for being in last_generation)
    return last_rank, mean_fitness, last_generation[0]


def random_being_of_target_length():
    return random_being(len(target.genotype))


configuration_space = product(
    mutation_function_space,
    maximum_number_of_mutations_space,
    mutation_probability_space,
    survival_percentile_space,
    initial_population_size_space,
    fitness_function_space
)

runs = map(lambda t: configure(*t), configuration_space)
performances = map(lambda r: (r, *asymptotic_average_fitness(r, number_of_runs_per_simulation)), runs)

for run, average_maximal_rank, asymptotic_fitness, sample_being in performances:
    print(run)
    print(f'\taverage maximal rank: {average_maximal_rank:.02f}')
    print(f'\tasymptotic fitness: {asymptotic_fitness:.02f}')
    print(f'\tsample being: {sample_being}')
