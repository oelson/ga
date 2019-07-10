from typing import List
from binascii import hexlify

from genetic_algorithm.mutation import random_mutation
from genetic_algorithm.genome import random_genome


class Being:
    """
    Un individu est caractérisé par son génome et son phénotype.
    """

    def __init__(self, genotype: bytearray, phenotype):
        self.genotype = genotype
        self.phenotype = phenotype

    def __str__(self):
        return f'{{phenotype:{repr(self.phenotype)}, genotype:{hexlify(self.genotype)}}}'

    def __repr__(self):
        return self.__str__()


Population = List[Being]


def random_population(population_size, genome_size) -> Population:
    """
    Population aléatoire de dimension et de taille de génome donnés.
    """
    genomes = (random_genome(genome_size) for _ in range(population_size))
    return [Being(g, express_genome_as_string(g)) for g in genomes]


def express_genome_as_string(genome: bytearray) -> str:
    """
    Exprime un génome en tant que chaîne de caractères unicode via un décodage UTF-8.
    """
    return bytes(genome).decode('UTF-8', 'replace')


def deduce_genome_from_string(string: str) -> bytearray:
    """
    Déduit un génome d'une chaîne de caractère via un encodage UTF-8.
    """
    return bytearray(string.encode('UTF-8', 'replace'))


def mutate_and_clone(being: Being, mutation_distribution: dict, fertility_rate: int) -> Population:
    """
    Le cycle de vie d'un individu est l'ensemble des individus qui procèdent de sa vie.
    """
    being = mutate_being(being, mutation_distribution)
    return [clone_being(being) for _ in range(fertility_rate)]


def mutate_being(being: Being, mutation_distribution: dict) -> Being:
    """
    Mutation aléatoire d'un individu selon une loi donnée.
    """
    mutation = random_mutation(mutation_distribution)
    being.genotype = mutation(being.genotype)
    return being


def clone_being(being: Being) -> Being:
    """
    Clonage.
    """
    genome_copy = bytearray(being.genotype)
    return Being(genome_copy, express_genome_as_string(genome_copy))


def random_being(genome_size: int) -> Being:
    """Individu aléatoire."""
    genome = random_genome(genome_size)
    return Being(genome, express_genome_as_string(genome))


def target_being(string: str) -> Being:
    """
    produit un individu cible à partir d'une chaîne de caractères donnée.
    """
    genome = deduce_genome_from_string(string)
    return Being(genome, express_genome_as_string(genome))
