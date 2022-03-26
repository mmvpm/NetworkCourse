import time
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    now = bytes(str(time.asctime()), 'utf-8')
    server_socket.sendto(now, ('<broadcast>', 12321))
    time.sleep(1)
