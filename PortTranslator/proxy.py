import socket
import requests

class ProxySocket:

    def __init__(self, from_host: str, from_port: int, to_host: str, to_port: int):
        self.to_url = f'http://{to_host}:{to_port}'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((from_host, from_port))
        self.socket.listen(1)
        self.launch()

    def __del__(self):
        self.socket.close()

    @staticmethod
    def ok_response(content: str):
        return bytes(f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}', 'utf-8')

    def handle_client(self, client_socket):
        client_socket.recv(1024)
        response = requests.get(self.to_url)
        response_decoded = response.content.decode(response.encoding or 'utf-8')
        client_socket.send(ProxySocket.ok_response(response_decoded))

    def launch(self):
        while True:
            client_socket, _ = self.socket.accept()
            self.handle_client(client_socket)
            client_socket.close()
