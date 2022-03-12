import socket

server_port = 12321

client_socket = socket.socket()
client_socket.connect(('localhost', server_port))

filename = 'C:/Users/Xiaomi/Desktop/Projects/Python/gen.py'
client_socket.sendall(bytes(f'GET /{filename} HTTP/1.1\r\n\r\n', 'utf-8'))

data = client_socket.recv(1024).decode('utf-8')
client_socket.close()

print(data)