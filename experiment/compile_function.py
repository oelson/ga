import marshal
from datetime import datetime
from os import stat
from py_compile import compile

'''
TODO use processes to isolate memory space & SIGSEGV errors
'''


def input():
    return [1, 6, 3, 7, 5, 9, 8, 2, 4, 10]


def original_genome():
    for i in range(1, len(l)):
        for j in range(i + 1, len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i]
    return l


def express(genome):
    l = input()
    exec(genome, {'l': l})
    return l


original_code = original_genome.__code__
original_result = express(original_code)
binary = marshal.dumps(original_code.co_code)

magic_number = int.from_bytes(binary[0:4], byteorder='little', signed=False)
modification_timestamp = int.from_bytes(binary[4:8], byteorder='little', signed=False)
source_size = int.from_bytes(binary[8:12], byteorder='little', signed=False)
original_bytecode = binary[12:]
modification_time = datetime.fromtimestamp(modification_timestamp)
print(f'magic number:      {magic_number:02x}')
print(f'modification time: {modification_time}')
print(f'source size:       {source_size:02x}')
print(f'input:             {input()}')
print(f'original result:   {original_result}')
print()

for byte_index in range(0, 2):
    original_byte = original_bytecode[byte_index]
    print(f'byte index: {byte_index}, value: 0x{original_byte:02x}')

    for random_byte in range(0xff + 1):
        print(f'\trandom byte: 0x{random_byte:02x} -> ', end='')

        mutated_bytecode = bytearray(original_bytecode)
        mutated_bytecode[byte_index] = random_byte

        try:
            mutated_code = marshal.loads(mutated_bytecode)
            # TODO fitness: number of numbers in ascending order
            # TODO label the code with a note (same, better, worse, malformed)
        except Exception as e:
            print(f'compile error: {e}')
            continue
            # TODO disasembly that tolerate fault
            # TODO diff disasemblies

        try:
            mutated_result = express(mutated_code)
        except Exception as e:
            print(f'exec error: {e}')
            continue

        print(mutated_result)
