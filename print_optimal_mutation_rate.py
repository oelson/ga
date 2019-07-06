"""
TODO introduire l'idée d'un nombre de mutations par génération :
TODO actuellement il y a 0 ou 1 mutation selon une probabilité, mais en vrai il peut y en avoir 40 par génération
"""

from genetic_algorithm.application.optimal_mutation_rate import compute_asymptotic_fitness
from numpy import linspace

simulation = compute_asymptotic_fitness(
    target_string='coucou',
    number_of_runs=1,
    population_size=30,
    fecondity_rate=2,
    mutation_probability_space=list(linspace(0.0, 1.0, 10)),
    # TODO donner les types de mutations dans une liste (sans no_mutation)
    maximum_rank=1000
)

for mutation_probability, average_maximal_rank, asymptotic_fitness, best_being, best_fitness in simulation():
    print(f'mutation probability: {mutation_probability:.02f}')
    print(f'\tasymptotic fitness: {asymptotic_fitness:.02f}')
    print(f'\taverage maximal rank: {average_maximal_rank:.02f}')
    print(f'\tbest being: {best_being}')
    print(f'\tbest fitness: {best_fitness}')
