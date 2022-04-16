import socket
from random import randint
from checksum import Checksum

ACK_SIZE = 3
HEADER_SIZE = 2
BATCH_SIZE = 1024

class StopAndWaitSocket:

    def __init__(self, timeout):
        self.checksum = Checksum()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.timeout = timeout
        self.socket.settimeout(timeout)

    def connect(self, host, port):
        self.connection = (host, port)

    def bind(self, host, port):
        self.socket.bind((host, port))

    def split_data(self, data: str) -> list[str]:
        return [
            data[i:i + BATCH_SIZE] 
            for i in range(0, len(data), BATCH_SIZE)
        ]

    def add_header(self, data: bytes, index: int) -> bytes:
        data = bytes([index]) + data
        checksum = self.checksum.compute(data)
        return bytes([checksum]) + data

    def build_ack(self, index: int) -> bytes:
        # f'{checksum}{index}ACK'
        return self.add_header(b'ACK', index)

    def build_packet(self, data: str, index: int) -> bytes:
        # f'{checksum}{index}{data}'
        return self.add_header(data.encode(encoding='utf-8'), index)

    def parse_packet(self, packet: bytes):
        return packet[0], packet[1], packet[2:].decode()

    def send(self, data: str):
        index = 1  # mod 2
        for i, packet in enumerate(self.split_data(data)):
            index = (index + 1) % 2
            packet = self.build_packet(packet, index)
            while True:
                self.socket.sendto(packet, self.connection)
                print(f'Packet #{i} with index = {index} has been sent.')
                try:
                    ack, _ = self.socket.recvfrom(HEADER_SIZE + ACK_SIZE)
                    if randint(1, 3) == 1:
                        raise socket.timeout()  # 30% lost
                    if ack == self.build_ack(index):
                        print(f'ACK with index = {index} has been received.')
                        break  # success
                except socket.timeout:
                    print('timed out')
                    continue  # to the next attempt

    def recv(self, left_data_size) -> str:
        expected_index = 0  # mod 2
        received_data = []

        while left_data_size > 0:
            try:
                packet, address = self.socket.recvfrom(HEADER_SIZE + BATCH_SIZE)
                _, cur_index, cur_data = self.parse_packet(packet)

                if randint(1, 3) == 1:
                    raise socket.timeout()  # 30% lost

                if cur_index == expected_index:
                    if not self.checksum.verify(packet):
                        print('incorrect checksum')
                        continue
                    expected_index = (cur_index + 1) % 2
                    received_data.append(cur_data)
                    left_data_size -= len(cur_data)
                    print(f'Packet with index = {cur_index} has been received: {len(cur_data)} byte(s).')

                self.socket.sendto(self.build_ack(cur_index), address)
                print(f'ACK with index = {cur_index} has been sent.')

            except socket.timeout:
                print('timed out')
                continue

        return ''.join(received_data)
