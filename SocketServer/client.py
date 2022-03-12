import socket
import argparse

from util import read_from_socket

server_port = 12321

def make_request(filename: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', server_port))
    client_socket.sendall(bytes(f'GET /{filename} HTTP/1.1\r\n\r\n', 'utf-8'))

    print(read_from_socket(client_socket))

    client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    make_request(args.filename)
