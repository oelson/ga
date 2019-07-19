from json import dumps as to_json
from statistics import mean
from itertools import product

from genetic_algorithm.mutation import Hazard, no_mutation, flip_random_bit_in_random_byte, random_byte_replacement, \
    Mutation
from genetic_algorithm.scenario.converge import ConvergeToTarget
from genetic_algorithm.selection import letter_distance, bytearray_distance, bytearray_bit_distance, Fitness
from genetic_algorithm.population import Being
from genetic_algorithm.species.unicode import target_text, random_being

target = target_text('cadavre')
number_of_runs_per_simulation = 3
maximum_rank = 1000
mutation_function_space = [flip_random_bit_in_random_byte]  # [flip_random_bit_in_random_byte, random_byte_replacement]
mutation_probability_space = [.3]  # [.7, .5, .3]
maximum_number_of_mutations_space = [1]  # [1, 2, 3]
initial_population_size_space = [20]  # [20, 50]
survival_percentile_space = [.5]  # [.5, .25]


def phenotype_comparison(b):
    return letter_distance(b.phenotype, target.phenotype)


def genotype_comparison(b):
    return bytearray_distance(b.genotype, target.genotype)


def fine_genotype_comparison(b):
    return bytearray_bit_distance(b.genotype, target.genotype)


fitness_function_space = [phenotype_comparison, genotype_comparison, fine_genotype_comparison]


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


def random_being_of_target_length() -> Being:
    return random_being(len(target.genotype))


def jsonify(run, average_maximal_rank, asymptotic_fitness, sample_being):
    return {
        'configuration': {
            'hazard': {
                'distribution': {
                    function.__name__: probability for function, probability in run.hazard.distribution.items()
                },
                'maximum': run.hazard.maximum
            },
            'fitness function': run._fitness.__name__,
            'survival percentile': run.survival_percentile,
            'initial population size': run.initial_population_size
        },
        'result': {
            'average maximal rank': average_maximal_rank,
            'asymptotic fitness': asymptotic_fitness,
            'sample being': sample_being.to_dict()
        }
    }


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
json_objects = list(map(lambda v: jsonify(*v), performances))

print(to_json(json_objects, indent=2))
