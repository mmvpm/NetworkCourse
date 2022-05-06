import time
import socket
from threading import Thread
from node import Node
from node_info import NodeInfo

# configuration

HOST = '127.0.0.1'

node_info_0 = NodeInfo('0', HOST, 12000)
node_info_1 = NodeInfo('1', HOST, 12001)
node_info_2 = NodeInfo('2', HOST, 12002)
node_info_3 = NodeInfo('3', HOST, 12003)

node_0 = Node(node_info_0, [node_info_1, node_info_2, node_info_3], {'1': 1, '2': 3, '3': 7})
node_1 = Node(node_info_1, [node_info_0, node_info_2], {'0': 1, '2': 1})
node_2 = Node(node_info_2, [node_info_0, node_info_1, node_info_3], {'0': 3, '1': 1, '3': 2})
node_3 = Node(node_info_3, [node_info_0, node_info_2], {'0': 7, '2': 2})

nodes = [node_0, node_1, node_2, node_3]

# starting synchronization

for node in nodes:
    Thread(target=node.sync).start()

time.sleep(5) # changing weights after that

main_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def set_new_weight(a: NodeInfo, b: NodeInfo, new_weight: int):
    global main_socket
    print(f'[Main] set {a.name} -> {b.name} weight to {new_weight}')
    main_socket.sendto(f'weight|{a.name}|{new_weight}'.encode(), (b.host, b.port))
    main_socket.sendto(f'weight|{b.name}|{new_weight}'.encode(), (a.host, a.port))

set_new_weight(node_info_1, node_info_2, 6)  # old value: 1
set_new_weight(node_info_0, node_info_2, 7)  # old value: 3
set_new_weight(node_info_0, node_info_3, 2)  # old value: 7

time.sleep(30) # stopping after that

for node in nodes:
    main_socket.sendto(b'stop||', (node.info.host, node.info.port))
