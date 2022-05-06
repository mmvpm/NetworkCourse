import ast
import copy
import socket
from dv import DistanceVector
from node_info import NodeInfo

class Node:

    def __init__(self, info: NodeInfo, neighbors: list[NodeInfo], weights: dict[str, int]):
        self.info = copy.deepcopy(info)
        self.neighbors = copy.deepcopy(neighbors)
        self.weights = copy.deepcopy(weights)

        self.info.dv[self.info.name] = 0
        self.info.which_neighbor[self.info.name] = self.info.name
        for neighbor in self.neighbors:
            self.info.dv[neighbor.name] = self.weights[neighbor.name]
        self.log(f'init dv: {self.info.dv}')

        self.send_socket_init()
        self.receive_socket_init()
        self.notify_neighbors()

    def send_socket_init(self):
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.send_socket.settimeout(0.1)

    def receive_socket_init(self):
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.settimeout(0.1)
        self.receive_socket.bind((self.info.host, self.info.port))

    def log(self, message: str):
        print(f'[Node "{self.info.name}"] {message}')

    def send(self, message: str, to_node: NodeInfo):
        self.send_socket.sendto(message.encode(), (to_node.host, to_node.port))

    def receive(self):
        try:
            request, _ = self.receive_socket.recvfrom(1024)
            return request.decode()
        except socket.timeout:
            pass

    def notify_neighbors(self):
        for to_neighbor in self.neighbors:
            # poisoning the way back
            dv_fixed = copy.copy(self.info.dv.data)
            for banned_node_name in self.info.which_neighbor:
                if self.info.which_neighbor[banned_node_name] == to_neighbor.name:
                    dv_fixed.pop(banned_node_name)

            message = f'dv|{self.info.name}|{dv_fixed}'
            self.send(message, to_neighbor)
    
    def handle_request(self, request: str):
        type, name, data = request.split('|')
        if type == 'weight':
            weight = int(data)
            self.set_neighbor_weight(name, weight)
        if type == 'dv':
            dv = ast.literal_eval(data)
            self.update_dv(name, dv)
        if type == 'stop':
            self.is_running = False

    def set_neighbor_weight(self, neighbor_name: str, new_weight: int):
        self.weights[neighbor_name] = new_weight
        self.info.dv[neighbor_name] = new_weight
        self.info.which_neighbor[neighbor_name] = neighbor_name
        self.log(f'weights has changed: {self.weights}')
        self.log(f'dv has changed: {self.info.dv}')

    def update_dv(self, neighbor_name: str, neighbor_dv: dict[str, int]):
        for neighbor in self.neighbors:
            if neighbor.name == neighbor_name:
                neighbor.dv.update_dv(neighbor_dv)
                break

    def recompute_dv(self):
        new_dv = DistanceVector()
        new_which_neighbor = {}

        new_dv[self.info.name] = 0
        new_which_neighbor[self.info.name] = self.info.name
        for neighbor in self.neighbors:
            c = self.weights[neighbor.name]
            for x in neighbor.dv.data:
                if new_dv.update_item(x, c + neighbor.dv[x]):
                    new_which_neighbor[x] = neighbor.name

        if self.info.dv.data != new_dv.data:
            self.info.dv = new_dv
            self.info.which_neighbor = new_which_neighbor
            self.log(f'dv has changed: {self.info.dv}')
            self.notify_neighbors()

    def sync(self):
        self.is_running = True
        iteration_number = 1
        while self.is_running:
            request = self.receive()
            if request is not None:
                self.handle_request(request)
                self.recompute_dv()
            if iteration_number % 50 == 0:
                self.log('scheduled notify_neighbors()')
                self.notify_neighbors()
            iteration_number += 1
        self.log(f'final dv: {self.info.dv}')
