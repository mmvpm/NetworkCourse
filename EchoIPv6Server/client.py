import socket

host = '::1'
port = 12321

client_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.settimeout(1)

message = 'sample message'
client_socket.sendto(message.encode(), (host, port))
print(f'Client: {message}')

try:
    response, _ = client_socket.recvfrom(1024)
    response = response.decode()
    print(f'Server: {response}')
except:
    print(f'Timed out\n')
