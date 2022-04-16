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

def send_to_server(host, port, timeout):
    client_data = read_file('data/client_data.txt')
    client_socket = stopnwait.StopAndWaitSocket(timeout)
    client_socket.connect(host, port)
    client_socket.send(client_data)
    print('Client data has been sent.')

def recv_from_server(host, port, timeout, total_data_size):
    client_socket = stopnwait.StopAndWaitSocket(timeout)
    client_socket.bind(host, port)
    received_server_data = client_socket.recv(total_data_size)
    write_file('data/received_server_data.txt', received_server_data)
    print(f'Server data has been received: {len(received_server_data)} byte(s).')

if __name__ == '__main__':
    host, port, timeout, total_data_size = parse_arguments()
    input('Press any key to start sending: ')
    send_to_server(host, port, timeout)
    input('Press any key to start receiving: ')
    recv_from_server(host, port, timeout, total_data_size)
