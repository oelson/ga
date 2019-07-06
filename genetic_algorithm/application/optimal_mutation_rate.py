from numpy import mean

from genetic_algorithm.selection import truncate, bytearray_bit_distance
from genetic_algorithm.mutation import no_mutation, random_byte_replacement, flit_random_bit_in_random_byte
from genetic_algorithm.population import generate, select_over_all_livings, any_perfect_being_in_population
from genetic_algorithm.scenario.unicode import Being, Population, random_population, target_being, being_lifecycle


def compute_asymptotic_fitness(
        target_string: str,
        number_of_runs: int,
        population_size: int,
        fecondity_rate: int,
        mutation_probability_space: list,
        maximum_rank: int) -> callable:
    """
    Obtient une fonction effectuant un nombre donné d'évolutions en vue de produire la mesure d'adaptation asymptotique
    moyenne pour un jeu de probabilités de mutations données.
    """
    target = target_being(target_string)
    survival_percentile = 1 / fecondity_rate

    def initial_population() -> Population:
        return random_population(population_size, len(target.genotype))

    def fitness(being: Being) -> float:
        return bytearray_bit_distance(being.genotype, target.genotype)
        # return bytearray_distance(being.genotype, target.genotype)

    def stop(rank: int, population: Population) -> bool:
        return rank == maximum_rank or any_perfect_being_in_population(population, fitness)

    def compute_average_asymptotic_fitness(mutation_distribution: dict):
        def lifecycle(population: Population) -> Population:
            return select_over_all_livings(
                population,
                lambda b: being_lifecycle(b, mutation_distribution, fecondity_rate),
                lambda p: truncate(p, fitness, survival_percentile))

        def describe_terminal_generation() -> (int, float, Being):
            generations = generate(
                initial_population(),
                lifecycle,
                stop)
            *_, (last_rank, last_generation) = generations
            asymptotic_fitness = mean([fitness(being) for being in last_generation])
            return last_rank, asymptotic_fitness, last_generation[0]

        def average_asymptotic_fitness_and_metadata() -> (int, float, Being):
            """
            Lance plusieurs calculs d'adaptation asymptotiques et retourne la moyenne.
            """
            runs = [describe_terminal_generation() for _ in range(number_of_runs)]

            average_asymptotic_fitness = mean([f for f, _, _ in runs])
            average_maximal_rank = mean([r for _, r, _ in runs])
            best_being = next(b for _, _, b in runs)

            return average_asymptotic_fitness, average_maximal_rank, best_being

        return average_asymptotic_fitness_and_metadata

    def build_mutation_distribution(mutation_probability: float) -> dict:
        # TODO diviser la probabilité de mutation en autant de types que souhaité
        # TODO par exemple mutation_probability = 0.20 avec deux types T1 et T2 -> {no_mutation: .80, T1: .10, T2: .10}
        return {
            no_mutation: 1 - mutation_probability,
            flit_random_bit_in_random_byte: mutation_probability,
            # random_byte_replacement: mutation_probability,
        }

    def values():
        """
        Effectue un calcul d'adaptation asymptotique moyen pour chaque probabilité au sein de l'espace de mutation.
        Produit la moyenne du rang maximal, l'adaptation asymptotique, le meilleur individu et son adaptation.
        """
        for mutation_probability in mutation_probability_space:
            mutation_distribution = build_mutation_distribution(mutation_probability)
            _simulation = compute_average_asymptotic_fitness(mutation_distribution)
            average_maximal_rank, asymptotic_fitness, best_being = _simulation()
            best_fitness = fitness(best_being)
            yield mutation_probability, average_maximal_rank, asymptotic_fitness, best_being, best_fitness

    return values
