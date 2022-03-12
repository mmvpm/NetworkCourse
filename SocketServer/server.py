import socket

server_port = 12321

def read_from_socket(socket):
    request = socket.recv(1024).decode('utf-8')
    return request.split(' ')[1][1:] # path to the local file

def read_from_file(path):
    try:
        with open(path, 'rt') as file:
            return file.read()
    except:
        return None

def bad_request_response():
    return b'HTTP/1.1 400 Bad Request\r\n\r\n'

def not_found_response():
    return b'HTTP/1.1 404 Not Found\r\n\r\n'

def ok_response(content):
    return bytes(f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}', 'utf-8')

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)

    while True:
        connection_socket, _ = server_socket.accept()
        print(connection_socket)

        try:
            path_to_file = read_from_socket(connection_socket)
            print('path:', path_to_file)
            file_content = read_from_file(path_to_file)
            if file_content is None:
                connection_socket.send(not_found_response())
            else:
                connection_socket.send(ok_response(file_content))
        except Exception as e:
            print(e)
            connection_socket.send(bad_request_response())

        connection_socket.close()

if __name__ == '__main__':
    main()