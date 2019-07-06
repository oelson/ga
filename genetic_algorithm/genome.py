from random import randint


def random_genome(size: int) -> bytearray:
    return bytearray(random_byte() for _ in range(size))


def random_byte_index(genotype: bytearray) -> int:
    return randint(0, len(genotype) - 1)


def random_bit_index_in_byte():
    return randint(0, 7)


def random_byte():
    return randint(0x00, 0xff)
