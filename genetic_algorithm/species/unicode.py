from genetic_algorithm.mutation import random_mutations
from genetic_algorithm.genome import random_genome
from genetic_algorithm.population import Being, Population


class TextBeing(Being):
    def __init__(self, genotye: bytearray):
        phenotype = genotye.decode('UTF-8', 'replace')
        super().__init__(genotye, phenotype)


def mutate_and_clone(
        being: Being,
        maximum_number_of_mutations: int,
        mutation_distribution: dict,
        fertility_rate: int) -> Population:
    being = mutate_being(being, maximum_number_of_mutations, mutation_distribution)
    return [clone_being(being) for _ in range(fertility_rate)]


def mutate_being(being: Being, maximum_number_of_mutations: int, mutation_distribution: dict) -> Being:
    for mutation in random_mutations(maximum_number_of_mutations, mutation_distribution):
        being.genotype = mutation(being.genotype)
    return being


def clone_being(being: Being) -> Being:
    genome_copy = bytearray(being.genotype)
    return TextBeing(genome_copy)


def random_being(genome_size: int) -> Being:
    genome = random_genome(genome_size)
    return TextBeing(genome)


def target_being(string: str) -> Being:
    genome = bytearray(string.encode('UTF-8', 'replace'))
    return TextBeing(genome)
