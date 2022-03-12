import socket

from util import *
from response import *

server_port = 12321

def get_path_from_socket(socket):
    request = read_from_socket(socket)
    return request.split(' ')[1][1:]

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)

    while True:
        connection_socket, address = server_socket.accept()
        print(f'Open connection to {address}')

        try:
            path_to_file = get_path_from_socket(connection_socket)
            print(f'Request: {path_to_file}')
            file_content = read_from_file(path_to_file)
            if file_content is None:
                connection_socket.send(not_found_response())
            else:
                connection_socket.send(ok_response(file_content))
        except Exception as e:
            print(e)
            connection_socket.send(bad_request_response())

        connection_socket.close()
        print(f'Close connection to {address}')

if __name__ == '__main__':
    main()