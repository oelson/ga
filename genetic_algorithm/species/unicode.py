from genetic_algorithm.genome import random_genome
from genetic_algorithm.population import Being, Population


class TextBeing(Being):
    def __init__(self, genotye: bytearray):
        phenotype = genotye.decode('UTF-8', 'replace')
        super().__init__(genotye, phenotype)

    def reproduce(self, population: Population):
        return clone_being(self)


def clone_being(being: Being) -> Being:
    genome_copy = bytearray(being.genotype)
    return TextBeing(genome_copy)


def random_being(genome_size: int) -> Being:
    genome = random_genome(genome_size)
    return TextBeing(genome)


def target_text(string: str) -> Being:
    genome = bytearray(string.encode('UTF-8', 'replace'))
    return TextBeing(genome)
