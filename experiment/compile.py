import marshal
import struct
import time
from os import stat
from py_compile import compile


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
    magic_number = genome_file.read(4)
    modification_timestamp = genome_file.read(4)
    source_size = genome_file.read(4)
    unknown_field = genome_file.read(4)
    original_bytecode = genome_file.read()

modification_time = time.asctime(time.localtime(struct.unpack('L', modification_timestamp)[0]))
original_code = marshal.loads(original_bytecode)
original_result = execute(original_code, input())

# inspect pyc
print(f'compiled {code_path} ({code_stat.st_size} bytes) to {genome_path} ({genome_stat.st_size} bytes)')
print(f'magic number:      0x{magic_number.hex()}')
print(f'modification time: {modification_time}')
print(f'source size:       0x{source_size.hex()}')
print(f'unknown field:     0x{unknown_field.hex()}')
print(f'input:             {input()}')
print(f'original result:   {original_result}')
print()

for random_byte in range(0xff + 1):
    print(f'random byte: 0x{random_byte:02x}')

    mutated_bytecode = bytearray(original_bytecode)
    mutated_bytecode[0] = random_byte

    try:
        mutated_code = marshal.loads(mutated_bytecode)
        mutated_result = execute(mutated_code, input())
        print(f'\tmutated result: {mutated_result}')
        # TODO fitness: number of numbers in ascending order
    except Exception as e:
        print(f'\terror: {e}')
        # TODO disasembly that tolerate fault
        # TODO diff disasemblies
