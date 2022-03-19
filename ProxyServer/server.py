import socket
import requests
import argparse

from util import *
from response import *
from logger import Logger
from blacklist import BlackList
from threadpool import ThreadPool

logger = Logger()
blacklist = BlackList()

server_port = 12321

def handle_client(socket, address):
    logger.info(f'Connection to {address} opened')

    try:
        request = read_from_socket(socket)

        method = request.split(' ')[0]
        requested_url = request.split(' ')[1][1:]
        logger.info(f'Requested URL: {requested_url}')

        request_body = None
        if '\r\n\r\n' in request:
            request_body = request[request.index('\r\n\r\n') + 2:]
            logger.info(f'Request body: {request_body}')

        if blacklist.is_banned(requested_url):
            logger.info(f'Requested URL is blacklisted')
            socket.send(ok_response('Requested URL is blacklisted'))
        else:
            response = requests.request(method, requested_url, data=request_body)
            logger.info(f'Response code: {response.status_code}')
            response_decoded = response.content.decode(response.encoding)
            socket.send(ok_response(response_decoded))
    except Exception as e:
        logger.info(e)
        socket.send(bad_request_response())

    socket.close()
    logger.info(f'Connection to {address} closed')

def main(nthreads):
    thread_pool = ThreadPool(nthreads, function=handle_client)
    thread_pool.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    logger.info('Server started')

    while True:
        try:
            thread_pool.push(server_socket.accept())
        except KeyboardInterrupt:
            break
    
    thread_pool.stop()
    logger.info('Server stopped')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nthreads', nargs='?', const=1, type=int, default=1)
    args = parser.parse_args()
    main(args.nthreads)
