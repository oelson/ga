from random import randint

from genetic_algorithm.population import Being, Population


class TextBeing(Being):
    def __init__(self, genotype: bytearray):
        phenotype = genotype.decode('UTF-8', 'replace')
        super().__init__(genotype, phenotype)

    def reproduce(self, population: Population):
        return clone_being(self)


def clone_being(being: Being) -> Being:
    genome_copy = bytearray(being.genotype)
    return TextBeing(genome_copy)


def random_being(genome_size: int) -> Being:
    genome = random_genome(genome_size)
    return TextBeing(genome)


def random_genome(size: int) -> bytearray:
    return bytearray(randint(0x00, 0xff) for _ in range(size))


def target_text(string: str) -> Being:
    genome = bytearray(string.encode('UTF-8', 'replace'))
    return TextBeing(genome)
