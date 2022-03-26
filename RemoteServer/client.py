import socket
import argparse

from util import read_from_socket

def make_request(host, port, command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(bytes(command, 'utf-8'))
    print(read_from_socket(client_socket))
    client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', const=1, type=str, default='localhost')
    parser.add_argument('--port', nargs='?', const=1, type=int, default=12321)
    parser.add_argument('--command', nargs='?', const=1, type=str, default="%windir%\system32\mspaint.exe")
    args = parser.parse_args()
    make_request(args.host, args.port, args.command)
