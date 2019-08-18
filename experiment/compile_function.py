import signal
from itertools import chain
from marshal import loads
from multiprocessing import Pool
from os import getpid, getppid
from py_compile import compile
from tempfile import NamedTemporaryFile
from typing import List, Tuple
from functools import partial


class BubleSort:
    PythonCode = '''
for i in range(0, len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] > numbers[j]:
            numbers[i], numbers[j] = numbers[j], numbers[i]
'''

    def __init__(self, bytecode, name):
        self.bytecode = bytecode
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def original():
        with NamedTemporaryFile(
                dir='/Users/nelson/Desktop/PYCOMPILE',
                suffix='.py',
                mode='w',
                encoding='utf-8',
                delete=False
        ) as source_file:
            source_file.write(BubleSort.PythonCode)

        code_file_path = compile(source_file.name, doraise=True)

        with open(code_file_path, 'rb') as code_file:
            # skip metadata
            code_file.seek(3 * 4)
            bytecode = code_file.read()

        return BubleSort(bytecode, 'original')

    def sort(self, numbers: List[int]):
        # kill(current_process().pid, signal.SIGSEGV)
        code = loads(self.bytecode)
        local_variables = {'numbers': numbers}
        exec(code, None, local_variables)
        return local_variables['numbers']


def print_and_exit(signum, frame):
    print(f'{getppid()}/{getpid()} caught signal {signal.Signals(signum).name} ({signum})', flush=True)
    # TODO comment terminer le processus pour qu'il soit recréé proprement ?


def initialize_process():
    for sig in (set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP}):
        signal.signal(sig, print_and_exit)


def safe_sort_10_elements(sort: BubleSort) -> (Tuple[int, int], BubleSort, List[int], Exception):
    pidinfo = (getpid(), getppid())
    numbers = [1, 6, 3, 7, 5, 9, 8, 2, 4, 10]
    try:
        return pidinfo, sort, sort.sort(numbers), None
    except Exception as exception:
        return pidinfo, sort, None, exception


def present_result(info, sort, sorted_numbers, error):
    (pid, ppid) = info
    if error:
        print(f'[{ppid}|{pid}] sort:{sort}, error:{error}', flush=True)
    else:
        print(f'[{ppid}|{pid}] sort:{sort}, numbers:{sorted_numbers}', flush=True)


# Compilation du tri original
original_sort = BubleSort.original()


# Mutation du tri original
def make_mutant(mutated_byte, byte_index):
    mutated_bytecode = bytearray(original_sort.bytecode)
    original_byte = mutated_bytecode[byte_index]
    mutated_bytecode[byte_index] = mutated_byte
    return BubleSort(mutated_bytecode, f'b#{byte_index}:{original_byte:02x}->{mutated_byte:02x}')


make_specific_mutant = partial(make_mutant, 0x00)

# Tris comme jeu de données
sorts = chain([original_sort], map(make_specific_mutant, range(0, 30)))

# Traitement parallèle du jeu de données
# TODO le premier processus qui plante semble figer l'ensemble du Pool
p = Pool(processes=4, maxtasksperchild=1, initializer=initialize_process)
results = p.map(safe_sort_10_elements, sorts)
for pidinfo, sort, sorted_numbers, exception in results:
    present_result(pidinfo, sort, sorted_numbers, exception)
p.close()
p.join()
