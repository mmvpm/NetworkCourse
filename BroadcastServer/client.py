import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client_socket.bind(('', 12321))
while True:
    now, _ = client_socket.recvfrom(1024)
    print(f'time: {now}')
