def read_from_socket(socket):
    batch_size = 1024
    result = []
    while True:
        batch = socket.recv(batch_size)
        result.extend(batch)
        if len(batch) < batch_size:
            break
    return bytes(result).decode('utf-8')

def read_from_file(path):
    try:
        with open(path, 'rt') as file:
            return file.read()
    except:
        return None
