import os
import socket
from util import *

server_port = 12321

def handle_client(socket):
    try:
        os.system(f'{read_from_socket(socket)} > out')
        socket.send(bytes(read_from_file('out'), encoding='utf-8'))
    except Exception as e:
        socket.send(bytes(str(e), encoding='utf-8'))
    socket.close()

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print(f'Server started at http://localhost:{server_port}/')

    while True:
        current_socket, _ = server_socket.accept()
        handle_client(current_socket)
