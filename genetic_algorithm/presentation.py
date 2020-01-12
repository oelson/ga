def binary_string(b: bytes):
    return ' '.join(bin(x)[2:].zfill(8) for x in b)


def byte_string(b: bytes):
    return ' '.join('{:02x}'.format(x) for x in b)