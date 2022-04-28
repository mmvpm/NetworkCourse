BASE = 16
BASE_BYTES = 2
MAX_BYTES = 2 ** BASE - 1

def checksum_compute(data: bytes) -> int:
    result = 0
    for i in range(0, len(data), BASE_BYTES):
        result += int.from_bytes(data[i:i + BASE_BYTES], 'little')
    while result & MAX_BYTES != result:
        result = (result >> BASE) + (result & MAX_BYTES)
    return MAX_BYTES ^ result

def checksum_verify(data: bytes) -> bool:
    return checksum_compute(data) == 0
