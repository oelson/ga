from random import choice, choices, randint
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

    @staticmethod
    def build(
            mutation_probability: float,
            mutation_distribution: Dict[Mutation, float],
            maximum_number_of_mutations: int):
        map_mutation_probability = {
            mutation: mutation_probability * inner_probability
            for mutation, inner_probability in mutation_distribution.items()
        }

        if mutation_probability < 1:
            map_mutation_probability[_no_mutation] = 1 - mutation_probability

        return Hazard(map_mutation_probability, maximum_number_of_mutations)


def replace_random_byte(genotype: bytearray) -> bytearray:
    index = _random_byte_index(genotype)
    genotype[index] = randint(0x00, 0xff)
    return genotype


def replace_random_bit(genotype: bytearray) -> bytearray:
    byte_index = _random_byte_index(genotype)
    byte = genotype[byte_index]
    bit_index = _random_bit_index_in_byte()
    mutated_byte = byte ^ (1 << bit_index)
    genotype[byte_index] = mutated_byte
    return genotype


def replace_random_letter(alphabet: str) -> Mutation:
    def mutate(genotype: bytearray) -> bytearray:
        text = genotype.decode('UTF-8', 'replace')
        new_text = _mutate_random_letter(text, alphabet)
        new_genome = new_text.encode('UTF-8', 'replace')
        return bytearray(new_genome)
    return mutate


def _no_mutation(genotype: bytearray) -> bytearray:
    return genotype


def _random_byte_index(genotype: bytearray) -> int:
    return randint(0, len(genotype) - 1)


def _random_bit_index_in_byte():
    return randint(0, 7)


def _mutate_random_letter(text: str, alphabet: str) -> str:
    letters = list(text)
    index = randint(0, len(letters) - 1)
    new_letter = choice(alphabet)
    letters[index] = new_letter
    new_text = ''.join(letters)
    return new_text
