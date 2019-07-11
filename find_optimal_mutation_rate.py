from numpy import linspace, mean

from genetic_algorithm.mutation import no_mutation, flit_random_bit_in_random_byte
from genetic_algorithm.scenario.converge import ConvergeToTarget


def measure(run: ConvergeToTarget):
    generations = run.generations()
    *_, (last_rank, last_generation) = generations
    asymptotic_fitness = float(mean([run.fitness(being) for being in last_generation]))
    return last_rank, asymptotic_fitness, last_generation[0]


def average(runs):
    measures = [measure(run) for run in runs]
    average_asymptotic_fitness = float(mean([f for f, _, _ in measures]))
    average_maximal_rank = float(mean([r for _, r, _ in measures]))
    sample_being = next(b for _, _, b in measures)
    return average_asymptotic_fitness, average_maximal_rank, sample_being


number_of_runs_per_simulation = 3
mutation_probability_space = list(linspace(0.01, 0.99, 3))

for mutation_probability in mutation_probability_space:
    mutation_distribution = {
        no_mutation: 1 - mutation_probability,
        flit_random_bit_in_random_byte: mutation_probability,
    }

    runs = [ConvergeToTarget(
        target_string='cadavre',
        survival_percentile=1 / 2,
        initial_population_size=50,
        maximum_number_of_mutations=2,
        mutation_distribution=mutation_distribution,
        maximum_rank=100
    ) for _ in range(number_of_runs_per_simulation)]

    average_maximal_rank, asymptotic_fitness, sample_being = average(runs)

    print(f'mutation probability: {mutation_probability:.02f}')
    print(f'\taverage maximal rank: {average_maximal_rank:.02f}')
    print(f'\tasymptotic fitness: {asymptotic_fitness:.02f}')
    print(f'\tsample being: {sample_being}')
