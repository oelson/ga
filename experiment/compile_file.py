import marshal
from datetime import datetime
from os import stat
from py_compile import compile

'''
TODO use processes to isolate memory space & SIGSEGV errors
'''


def input():
    return [1, 6, 3, 7, 5, 9, 8, 2, 4, 10]


def execute(code, list):
    l = {'list': list}
    exec(code, None, l)
    return l['list']


code_path = 'genome.py'

# compilation & stats
code_stat = stat(code_path)
genome_path = compile(code_path, doraise=True)
genome_stat = stat(genome_path)

# read bytecode
with open(genome_path, 'rb') as genome_file:
    magic_number = int.from_bytes(genome_file.read(4), byteorder='little', signed=False)
    modification_timestamp = int.from_bytes(genome_file.read(4), byteorder='little', signed=False)
    source_size = int.from_bytes(genome_file.read(4), byteorder='little', signed=False)
    original_bytecode = genome_file.read()

modification_time = datetime.fromtimestamp(modification_timestamp)
original_code = marshal.loads(original_bytecode)
original_result = execute(original_code, input())

# inspect pyc
print(f'compiled {code_path} ({code_stat.st_size} bytes) to {genome_path} ({genome_stat.st_size} bytes)')
print(f'magic number:      {magic_number:02x}')
print(f'modification time: {modification_time}')
print(f'source size:       {source_size:02x}')
print(f'input:             {input()}')
print(f'original result:   {original_result}')
print()

all_bytes = list(range(0xff + 1))

for byte_index in (0, 14):
    original_byte = original_bytecode[byte_index]
    print(f'byte index: {byte_index}, value: 0x{original_byte:02x}')

    for random_byte in all_bytes:

        mutated_bytecode = bytearray(original_bytecode)
        mutated_bytecode[byte_index] = random_byte
        print(f'\trandom byte: 0x{random_byte:02x} -> ', end='')
        try:
            mutated_code = marshal.loads(mutated_bytecode)
            mutated_result = execute(mutated_code, input())
            print(mutated_result)
            # TODO fitness: number of numbers in ascending order
            # TODO label the code with a note (same, better, worse, malformed)
        except Exception as e:
            print(e)
            # TODO disasembly that tolerate fault
            # TODO diff disasemblies
