from itertools import chain


def generate(initial_population: list, lifecycle: callable, stop: callable):
    rank, population = 1, initial_population
    yield rank, population

    while not stop(rank, population):
        rank, population = rank + 1, lifecycle(population)
        yield rank, population


def select_over_all_livings(population: list, being_lifecycle: callable, selection: callable) -> list:
    being_lifecycles = map(being_lifecycle, population)
    all_lives = list(chain.from_iterable(being_lifecycles))
    return selection(all_lives)
