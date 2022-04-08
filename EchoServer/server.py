import time
import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 12321))

while True:
    request, address = server_socket.recvfrom(1024)
    if random.randint(0, 99) < 20:
        continue
    time.sleep(random.random()) # delay for rtt != 0
    response = request.decode().upper().encode()
    server_socket.sendto(response, address)
