import socket

host = '::1'
port = 12321

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))

while True:
    request, address = server_socket.recvfrom(1024)
    request = request.decode()
    print(f'Client: {request}')
    
    response = request.upper()
    server_socket.sendto(response.encode(), address)
    print(f'Server: {response}')
