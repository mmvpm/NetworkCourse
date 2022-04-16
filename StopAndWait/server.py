import argparse
import stopnwait
from file import *

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', const=1, default='127.0.0.1', type=str)
    parser.add_argument('--port', nargs='?', const=1, default=12321, type=int)
    parser.add_argument('--timeout', nargs='?', const=1, default=1, type=int)
    parser.add_argument('--total_data_size', nargs='?', const=1, default=3599, type=int)
    args = parser.parse_args()
    return args.host, args.port, args.timeout, args.total_data_size

def recv_from_client(host, port, timeout, total_data_size):
    server_socket = stopnwait.StopAndWaitSocket(timeout)
    server_socket.bind(host, port)
    received_client_data = server_socket.recv(total_data_size)
    write_file('data/received_client_data.txt', received_client_data)
    print(f'Client data has been received: {len(received_client_data)} byte(s).')

def send_to_client(host, port, timeout):
    server_data = read_file('data/server_data.txt')
    server_socket = stopnwait.StopAndWaitSocket(timeout)
    server_socket.connect(host, port)
    server_socket.send(server_data)
    print('Server data has been sent.')

if __name__ == '__main__':
    host, port, timeout, total_data_size = parse_arguments()
    input('Press any key to start receiving: ')
    recv_from_client(host, port, timeout, total_data_size)
    input('Press any key to start sending: ')
    send_to_client(host, port, timeout)
