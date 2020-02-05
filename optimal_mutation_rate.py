from itertools import product
from json import dumps as to_json
from statistics import mean

from genetic_algorithm import mutation
from genetic_algorithm.population import Being
from genetic_algorithm.simulation import Simulation
from genetic_algorithm.presentation import binary_string
from genetic_algorithm.species.text import TextTarget

target = TextTarget('cadavre', 'UTF-8')
maximum_rank = 1000
number_of_runs_per_simulation = 2
fitness_function_space = [target.fitness_by_phenotype, target.fitness_by_genotype]
mutation_function_space = [mutation.replace_random_bit, mutation.replace_random_byte]
mutation_probability_space = [.7, .3]
maximum_number_of_mutations_space = [1, 3]
initial_population_size_space = [20, 50]
survival_percentile_space = [.5, .25]


def qualify(run: Simulation, number_of_runs: int) -> (float, float, Being):
    """Qualifie une simulation en produisant des statistiques et un échantillon."""
    measures = [fitness_of_last_generation(run) for _ in range(number_of_runs)]

    average_asymptotic_fitness = mean(f for f, _, _ in measures)
    average_maximal_rank = mean(r for _, r, _ in measures)
    sample_being = next(b for _, _, b in measures)

    return average_asymptotic_fitness, average_maximal_rank, sample_being


def fitness_of_last_generation(run: Simulation) -> (int, float, Being):
    last_rank, last_generation = run.last_generation()
    mean_fitness = mean(run.fitness(being) for being in last_generation)
    return last_rank, mean_fitness, last_generation[0]


# L'espace de configuration est l'ensemble des combinaisons possibles des paramètres
configuration_space = product(
    mutation_function_space,
    maximum_number_of_mutations_space,
    mutation_probability_space,
    survival_percentile_space,
    initial_population_size_space,
    fitness_function_space
)

# Pour chaque combinaison de configuration possible
for (mutation_function,
     maximum_number_of_mutations,
     mutation_probability,
     survival_percentile,
     initial_population_size,
     fitness_function) in configuration_space:
    # Instancie une simulation
    simulation = Simulation(
        initial_being=target.random_being,
        initial_population_size=initial_population_size,
        survival_percentile=survival_percentile,
        hazard=mutation.Hazard.build(mutation_probability, {mutation_function: 1}, maximum_number_of_mutations),
        fitness=fitness_function,
        maximum_rank=maximum_rank
    )

    # Test plusieurs fois la simulation et produit ses statistiques
    average_maximal_rank, asymptotic_fitness, sample_being = qualify(simulation, number_of_runs_per_simulation)

    # Affiche un résumé de la simulation et de ses résultats
    print(to_json({
        'configuration': {
            'hazard': {
                'distribution': {
                    function.__name__: probability for function, probability in simulation.hazard.distribution.items()
                },
                'maximum': simulation.hazard.maximum
            },
            'fitness function': simulation.fitness_function.__name__,
            'survival percentile': simulation.survival_percentile,
            'initial population size': simulation.initial_population_size
        },
        'result': {
            'average maximal rank': average_maximal_rank,
            'asymptotic fitness': asymptotic_fitness,
            'sample being': {
                'phenotype': sample_being.phenotype,
                'genotype': binary_string(sample_being.genotype)
            }
        }
    }, indent=2))
