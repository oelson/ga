from difflib import ndiff
from itertools import zip_longest


def truncate(population: list, fitness: callable, survival_percentile: float) -> list:
    competition = sorted(population, key=fitness)
    threshold = int(len(population) * survival_percentile)
    return competition[:threshold]


def letter_distance(a: str, b: str) -> int:
    """Compte le nombre de lettres différentes entre deux textes de mêmes tailles."""
    return sum(1 for la, lb in zip(a, b) if a != b)


def letter_distance_diff(a: str, b: str) -> int:
    """Compte le nombre de lettres différentes entre deux textes qui peuvent être de tailles différentes."""
    return sum(1 for charinfo in ndiff(a, b) if not charinfo.startswith(' '))


def bit_distance(a: int, b: int) -> int:
    """Compte le nombre de bits différents entre deux entiers qui peuvent être de tailles différentes. Approximatif."""
    x = a ^ b
    number_of_ones = sum((x >> shift) & 1 for shift in range(0, x.bit_length() + 1))
    length_difference = abs(a.bit_length() - b.bit_length())
    return number_of_ones + length_difference


def bytearray_distance(g1: bytearray, g2: bytearray):
    """Compte le nombre d'octets différents entre deux vecteurs qui peuvent être de tailles différentes."""
    return sum(1 for b1, b2 in zip_longest(g1, g2) if b1 != b2)


def bytearray_bit_distance(g1: bytearray, g2: bytearray):
    """Compte le nombre de bits différents entre deux vecteurs qui peuvent être de tailles différentes."""
    return sum(bit_distance(b1, b2) if b1 is not None and b2 is not None else 8 for b1, b2 in zip_longest(g1, g2))
