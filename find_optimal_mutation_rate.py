from numpy import linspace, mean

from genetic_algorithm.selection import truncate, bytearray_bit_distance
from genetic_algorithm.mutation import no_mutation, random_byte_replacement, flit_random_bit_in_random_byte
from genetic_algorithm.population import generate, select_over_all_livings
from genetic_algorithm.scenario.unicode import Being, Population, random_being, target_being, mutate_and_clone


# TODO Grouper ce qui est commun avec l'autre script dans une classe qui expose ces fonctions
# Une classe étant une collection de fonctions préparées, l'usage est adéquat \o/

def compute_average_asymptotic_fitness(mutation_distribution: dict):
    def initial_population() -> Population:
        return [random_being(len(target.genotype)) for _ in range(initial_population_size)]

    def fitness(b: Being) -> float:
        return bytearray_bit_distance(b.genotype, target.genotype)

    def select(p: Population) -> Population:
        return truncate(p, fitness, survival_percentile)

    def stop(r: int, p: Population) -> bool:
        return r == maximum_rank or not p or any(fitness(being) == 0 for being in p)

    def life(b: Being) -> Population:
        return mutate_and_clone(b, maximum_number_of_mutations, mutation_distribution, fertility_rate)

    def lifecycle(p: Population) -> Population:
        return select_over_all_livings(p, life, select)

    def perform():
        generations = generate(initial_population(), lifecycle, stop)
        *_, (last_rank, last_generation) = generations
        asymptotic_fitness = float(mean([fitness(being) for being in last_generation]))
        return last_rank, asymptotic_fitness, last_generation[0]

    # Lance N calculs de performance
    performances = [perform() for _ in range(number_of_runs_per_simulation)]

    # Rapporte les moyennes des résultats
    average_asymptotic_fitness = float(mean([f for f, _, _ in performances]))
    average_maximal_rank = float(mean([r for _, r, _ in performances]))
    sample_being = next(b for _, _, b in performances)

    return average_asymptotic_fitness, average_maximal_rank, sample_being


target = target_being('coucou')
initial_population_size = 30
survival_percentile = .5
fertility_rate = int(1 / survival_percentile)
maximum_number_of_mutations = 2
mutation_probability_space = list(linspace(0.01, 0.99, 10))
mutation_function = flit_random_bit_in_random_byte
number_of_runs_per_simulation = 5
maximum_rank = 200

for mutation_probability in mutation_probability_space:
    mutation_distribution = {
        no_mutation: 1 - mutation_probability,
        mutation_function: mutation_probability,
    }

    average_maximal_rank, asymptotic_fitness, sample_being = compute_average_asymptotic_fitness(mutation_distribution)

    print(f'mutation probability: {mutation_probability:.02f}')
    print(f'\taverage maximal rank: {average_maximal_rank:.02f}')
    print(f'\tasymptotic fitness: {asymptotic_fitness:.02f}')
    print(f'\tsample being: {sample_being}')
