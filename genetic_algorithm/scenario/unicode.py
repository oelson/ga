from typing import List
from binascii import hexlify

from genetic_algorithm.mutation import random_mutations
from genetic_algorithm.genome import random_genome


class Being:
    def __init__(self, genotype: bytearray, phenotype: str):
        self.genotype = genotype
        self.phenotype = phenotype

    def __str__(self):
        return f'{{phenotype:{repr(self.phenotype)}, genotype:{hexlify(self.genotype)}}}'

    def __repr__(self):
        return self.__str__()


Population = List[Being]


def express_genome_as_string(genome: bytearray) -> str:
    return bytes(genome).decode('UTF-8', 'replace')


def deduce_genome_from_string(string: str) -> bytearray:
    return bytearray(string.encode('UTF-8', 'replace'))


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
    return Being(genome_copy, express_genome_as_string(genome_copy))


def random_being(genome_size: int) -> Being:
    genome = random_genome(genome_size)
    return Being(genome, express_genome_as_string(genome))


def target_being(string: str) -> Being:
    genome = deduce_genome_from_string(string)
    return Being(genome, express_genome_as_string(genome))
