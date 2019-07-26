from random import choices, randint
from typing import Dict, Callable, Sequence

Mutation = Callable[[bytearray], bytearray]


class Hazard:
    def __init__(self, distribution: Dict[Mutation, float], maximum: int):
        self.distribution = distribution
        self.maximum = maximum

    def __call__(self, genotype: bytearray) -> bytearray:
        for mutation in self.pick():
            genotype = mutation(genotype)
        return genotype

    def pick(self) -> Sequence[Mutation]:
        return choices(
            population=list(self.distribution.keys()),
            weights=list(self.distribution.values()),
            k=self.maximum)


def no_mutation(genotype: bytearray) -> bytearray:
    return genotype


def random_byte_replacement(genotype: bytearray) -> bytearray:
    index = random_byte_index(genotype)
    genotype[index] = randint(0x00, 0xff)
    return genotype


def build_distribution(mutation_probability: float, mutation_distribution: Dict[Mutation, float]):
    mutation_distribution = {
        mutation: mutation_probability * inner_probability
        for mutation, inner_probability in mutation_distribution.items()
    }
    if mutation_probability < 1:
        mutation_distribution[no_mutation] = 1 - mutation_probability
    return mutation_distribution


def flip_random_bit_in_random_byte(genotype: bytearray) -> bytearray:
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
