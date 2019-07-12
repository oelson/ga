from random import choices, randint

from genetic_algorithm.population import Being


def mutate_being(being: Being, maximum_number_of_mutations: int, mutation_distribution: dict) -> Being:
    for mutation in random_mutations(maximum_number_of_mutations, mutation_distribution):
        being.genotype = mutation(being.genotype)
    return being


def random_mutations(maximum_number_of_mutations, distribution: dict) -> callable:
    mutations = choices(
        population=list(distribution.keys()),
        weights=list(distribution.values()),
        k=maximum_number_of_mutations)
    return mutations


def no_mutation(genotype: bytearray) -> bytearray:
    return genotype


def random_byte_replacement(genotype: bytearray) -> bytearray:
    index = random_byte_index(genotype)
    genotype[index] = randint(0x00, 0xff)
    return genotype


def flit_random_bit_in_random_byte(genotype: bytearray) -> bytearray:
    byte_index = random_byte_index(genotype)
    byte = genotype[byte_index]
    bit_index = random_bit_index_in_byte()
    mutated_byte = byte ^ (1 << bit_index)
    genotype[byte_index] = mutated_byte
    return genotype


def random_byte_index(genotype: bytearray) -> int:
    return randint(0, len(genotype) - 1)


def random_bit_index_in_byte():
    return randint(0, 7)
