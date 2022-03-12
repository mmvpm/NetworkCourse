import socket
import argparse

from util import *
from response import *
from ThreadPool import ThreadPool

server_port = 12321

def handle_client(socket, address):
    print(f'Connection to {address} opened')

    try:
        path_to_file = read_from_socket(socket).split(' ')[1][1:]
        print(f'Request: {path_to_file}')
        file_content = read_from_file(path_to_file)
        if file_content is None:
            socket.send(not_found_response())
        else:
            socket.send(ok_response(file_content))
    except Exception as e:
        print(e)
        socket.send(bad_request_response())

    socket.close()
    print(f'Connection to {address} closed')

def main(nthreads):
    thread_pool = ThreadPool(nthreads, function=handle_client)
    thread_pool.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print('Server started')

    while True:
        try:
            thread_pool.push(server_socket.accept())
        except KeyboardInterrupt:
            break
    
    thread_pool.stop()
    print('Server stopped')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nthreads', type=int)
    args = parser.parse_args()
    main(args.nthreads)
