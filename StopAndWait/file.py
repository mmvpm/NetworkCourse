def read_file(file_name):
    with open(file_name, 'rt', encoding='utf-8') as file:
        return file.read()

def write_file(file_name, data):
    with open(file_name, 'wt', encoding='utf-8') as file:
        return file.write(data)
