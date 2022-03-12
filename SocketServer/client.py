import socket
import argparse

from util import read_from_socket

def make_request(host, port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(bytes(f'GET /{filename} HTTP/1.1\r\n\r\n', 'utf-8'))

    print(read_from_socket(client_socket))

    client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('filename', type=str)

    args = parser.parse_args()

    make_request(args.host, args.port, args.filename)
