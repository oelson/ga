from marshal import loads
from py_compile import compile
from tempfile import NamedTemporaryFile

from genetic_algorithm.population import Being, Population


class PythonBeing(Being):
    def __init__(self, genotype: bytearray):
        # expression du génome par exécution du bytecode
        code = loads(genotype)
        # TODO process
        local_variables = {'numbers': [1, 6, 3, 7, 5, 9, 8, 2, 4, 10]}
        exec(code, None, local_variables)
        phenotype = local_variables['numbers']
        super().__init__(genotype, phenotype)

    def reproduce(self, population: Population):
        # clonage
        genome_copy = bytearray(self.genotype)
        return PythonBeing(genome_copy)


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
