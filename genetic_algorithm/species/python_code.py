from marshal import loads
from py_compile import compile
from tempfile import NamedTemporaryFile
from multiprocessing import Process, Queue

from genetic_algorithm.population import Being, Population


class PythonBeing(Being):
    def __init__(self, genotype: bytearray):
        # le code est exécuté au sein d'un processus séparé pour isoler ldes signaux tels SEGSIGV
        q = Queue()
        p = Process(target=evaluate_sort_bytecode, args=(q, genotype))
        p.start()
        phenotype, error = q.get()
        p.join()
        if error: raise error
        super().__init__(genotype, phenotype)


def clone_being(being: Being, population: Population):
    genome_copy = bytearray(being.genotype)
    return PythonBeing(genome_copy)


def evaluate_sort_bytecode(queue: Queue, genotype: bytearray):
    try:
        code = loads(genotype)
        local_variables = {'numbers': [1, 6, 3, 7, 5, 9, 8, 2, 4, 10]}
        exec(code, None, local_variables)
        phenotype = local_variables['numbers']
        queue.put((phenotype, None))
    except Exception as error:
        queue.put((None, error))


def source_code_to_bytecode(python_code: str, compile_directory: str) -> bytes:
    # write code to a temporary file
    source_file = NamedTemporaryFile(
        dir=compile_directory,
        suffix='.py',
        mode='w',
        encoding='utf-8',
        delete=False
    )

    with source_file:
        source_file.write(python_code)

    # compile the code
    code_file_path = compile(source_file.name, doraise=True)

    # read compilation output
    with open(code_file_path, 'rb') as code_file:
        # skip metadata
        code_file.seek(3 * 4)
        return code_file.read()
