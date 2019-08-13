from genetic_algorithm import selection
from genetic_algorithm.population import Being, random_genome, Population


class TextBeing(Being):
    def __init__(self, genotype: bytearray):
        phenotype = genotype.decode('UTF-8', 'replace')
        super().__init__(genotype, phenotype)


class TextTarget:
    def __init__(self, text):
        genome = bytearray(text.encode('UTF-8', 'replace'))
        self.being = TextBeing(genome)

    def fitness_by_genotype(self, being: Being):
        return selection.bytearray_bit_distance(being.genotype, self.being.genotype)

    def fitness_by_phenotype(self, being: Being):
        return selection.letter_distance(being.phenotype, self.being.phenotype)

    def random_being(self):
        genome = random_genome(len(self.being.genotype))
        return TextBeing(genome)


def clone_being(being: Being, population: Population) -> Being:
    genome_copy = bytearray(being.genotype)
    return TextBeing(genome_copy)
