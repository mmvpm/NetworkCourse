from checksum import Checksum

def test_base_8_happy_path():
    checksum = Checksum(base=8)
    data = b'qwerty123'
    result = checksum.compute(data)
    data_with_sum = bytes([result]) + data
    assert checksum.verify(data_with_sum)

def test_base_16_happy_path():
    checksum = Checksum(base=16)
    data = b'qwerty123'
    result = checksum.compute(data)
    data_with_sum = result.to_bytes(2, byteorder='big') + data
    assert checksum.verify(data_with_sum)

def test_base_32_happy_path():
    checksum = Checksum(base=32)
    data = b'qwerty123'
    result = checksum.compute(data)
    data_with_sum = result.to_bytes(4, byteorder='big') + data
    assert checksum.verify(data_with_sum)

def test_base_8_corrupted_data():
    checksum = Checksum(base=8)
    data = b'qwerty123'
    result = checksum.compute(data)
    data_with_sum = bytes([result + 1]) + data
    assert not checksum.verify(data_with_sum)

def test_base_16_corrupted_data():
    checksum = Checksum(base=16)
    data = b'qwerty123'
    result = checksum.compute(data)
    data_with_sum = result.to_bytes(2, byteorder='little') + data
    assert not checksum.verify(data_with_sum)

def test_base_32_corrupted_data():
    checksum = Checksum(base=32)
    data = b'qwerty123'
    result = checksum.compute(data)
    data_with_sum = (result + 1).to_bytes(4, byteorder='big') + data
    assert not checksum.verify(data_with_sum)
