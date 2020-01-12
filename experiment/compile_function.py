import signal
from marshal import loads
from multiprocessing import Process, Queue
from os import getpid, getppid, kill
from py_compile import compile
from sys import exit
from tempfile import NamedTemporaryFile
from typing import List


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
        code = loads(self.bytecode)
        local_variables = {'numbers': numbers}
        exec(code, None, local_variables)
        return local_variables['numbers']

    def present_result(self, numbers, error):
        if error:
            print(f'{self.name}, error:{error}', flush=True)
        else:
            print(f'{self.name}, numbers:{numbers}', flush=True)

    def present_crash(self, p: Process):
        print(f'{self.name}, exit:{p.exitcode}', flush=True)

    def mute(self, b: int, i: int):
        mutant = bytearray(self.bytecode)
        original_byte = mutant[i]
        mutant[i] = b
        return BubleSort(mutant, f'sort#{i}:{original_byte:02x}->{b:02x}')


def abort(signum, _):
    print(f'{getpid()}: {signum}', flush=True)
    # exit(1)
    kill(getpid(), signal.SIGINT)


def initialize_process(s: BubleSort):
    print(f'init process {getpid()} (parent {getppid()}) for sort {s}', flush=True)

    for s in signal.Signals:
        signal.signal(s, signal.SIG_DFL)

    signal.signal(signal.SIGSEGV, abort)


def safe_sort_10_elements(s: BubleSort, q: Queue) -> (List[int], Exception):
    initialize_process(s)
    n = [1, 6, 3, 7, 5, 9, 8, 2, 4, 10]
    try:
        m = s.sort(n)
    except Exception as e:
        q.put((None, e))
    else:
        q.put((m, None))


def sort_10_elements_in_subprocess(s: BubleSort) -> (BubleSort, List[int], Exception):
    q = Queue(maxsize=1)
    p = Process(target=safe_sort_10_elements, name=s.name, args=(s, q))
    p.start()
    try:
        n, e = q.get(timeout=.25)
        return s, n, e
    except Exception as e:
        return s, None, e
    finally:
        q.close()
        p.join()


original_sort = BubleSort.original()

sorts = [original_sort.mute(0x01, i) for i in range(0, 10)]

results = map(sort_10_elements_in_subprocess, sorts)

for s, n, e in results:
    s.present_result(n, e)
