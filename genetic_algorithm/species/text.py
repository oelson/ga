from random import randint

from genetic_algorithm import selection
from genetic_algorithm.population import Being, Population


class TextBeing(Being):
    def __init__(self, genotype: bytearray, encoding):
        phenotype = genotype.decode(encoding, 'replace')
        super().__init__(genotype, phenotype)
        self.encoding = encoding

    def reproduce(self, _: Population) -> Being:
        genome_copy = bytearray(self.genotype)
        clone = TextBeing(genome_copy, self.encoding)
        return clone


class TextTarget:
    def __init__(self, text, encoding):
        genome = bytearray(text.encode(encoding, 'replace'))
        self.being = TextBeing(genome, encoding)

    def fitness_by_genotype(self, being: Being):
        return selection.bytearray_bit_distance(being.genotype, self.being.genotype)

    def fitness_by_phenotype(self, being: Being):
        return selection.letter_distance(being.phenotype, self.being.phenotype)

    def random_being(self):
        genome = random_genome(len(self.being.genotype))
        return TextBeing(genome, self.being.encoding)

    def alphabet(self):
        return list(set(self.being.phenotype))


def random_genome(size: int) -> bytearray:
    return bytearray(randint(0x00, 0xff) for _ in range(size))
