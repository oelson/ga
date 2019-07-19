from random import randint

from genetic_algorithm.population import Being, Population
from genetic_algorithm import selection


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


class TextTarget:
    def __init__(self, text):
        self.being = target_text(text)

    def fitness_by_genotype(self, being: Being):
        return selection.bytearray_bit_distance(being.genotype, self.being.genotype)

    def fitness_by_phenotype(self, being: Being):
        return selection.letter_distance(being.phenotype, self.being.phenotype)

    def random_being(self):
        return random_being(len(self.being.genotype))
