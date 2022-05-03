import socket

import pygame
from config import *
from paint_base import PaintBase

class PaintServer(PaintBase):

    def socket_init(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1 / 30)
        self.socket.bind((HOST, PORT))

    def action_receive(self):
        request, _ = self.socket.recvfrom(1024)
        return request.decode().split()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                break

        try:
            action = self.action_receive()
        except socket.timeout:
            return

        if action[0] == 'quit':
            self.is_running = False

        if action[0] == 'mbd':
            self.mouse_pressed = True
            x, y = map(int, action[1:])
            self.draw_point(x, y)

        if action[0] == 'mbu':
            self.last_point = None
            self.mouse_pressed = False

        if action[0] == 'mm' and self.mouse_pressed:
            x, y = map(int, action[1:])
            self.draw_point(x, y)


if __name__ == '__main__':
    PaintServer().run()
