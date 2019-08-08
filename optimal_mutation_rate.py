from itertools import product
from json import dumps as to_json
from statistics import mean

from genetic_algorithm.mutation import Hazard, build_distribution, flip_random_bit_in_random_byte, Mutation
from genetic_algorithm.population import Being
from genetic_algorithm.scenario.converge import Converge
from genetic_algorithm.selection import Fitness
from genetic_algorithm.species.unicode import TextTarget

target = TextTarget('cadavre')
number_of_runs_per_simulation = 3
maximum_rank = 1000
mutation_function_space = [flip_random_bit_in_random_byte]  # [flip_random_bit_in_random_byte, random_byte_replacement]
mutation_probability_space = [.3]  # [.7, .5, .3]
maximum_number_of_mutations_space = [1]  # [1, 2, 3]
initial_population_size_space = [20]  # [20, 50]
survival_percentile_space = [.5]  # [.5, .25]

fitness_function_space = [target.fitness_by_phenotype, target.fitness_by_genotype]


def configure(
        mutation_function: Mutation,
        maximum_number_of_mutations: int,
        mutation_probability: float,
        survival_percentile: float,
        initial_population_size: int,
        fitness_function: Fitness
):
    mutation_distribution = build_distribution(mutation_probability, {mutation_function: 1})
    return Converge(
        initial_being=target.random_being,
        initial_population_size=initial_population_size,
        survival_percentile=survival_percentile,
        hazard=Hazard(mutation_distribution, maximum_number_of_mutations),
        fitness=fitness_function,
        maximum_rank=maximum_rank
    )


def asymptotic_average_fitness(run: Converge, number_of_runs: int) -> (float, float, Being):
    measures = [last_generation_fitness(run) for _ in range(number_of_runs)]

    average_asymptotic_fitness = mean(f for f, _, _ in measures)
    average_maximal_rank = mean(r for _, r, _ in measures)
    sample_being = next(b for _, _, b in measures)

    return average_asymptotic_fitness, average_maximal_rank, sample_being


def last_generation_fitness(run: Converge) -> (int, float, Being):
    last_rank, last_generation = run.last_generation()
    mean_fitness = mean(run.fitness(being) for being in last_generation)
    return last_rank, mean_fitness, last_generation[0]


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
