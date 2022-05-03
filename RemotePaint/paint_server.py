import pygame
import socket
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

    def draw_point(self, x, y):
        pygame.draw.circle(self.window, COLOR_BLACK, (x, y), BRUSH_THICKNESS)

    def draw_line(self, x0, y0, x1, y1):
        pygame.draw.line(self.window, COLOR_BLACK, (x0, y0), (x1, y1), BRUSH_THICKNESS + 1)

    def update(self):
        super().update()

        try:
            action = self.action_receive()
        except socket.timeout:
            return

        if action[0] == 'quit':
            self.is_running = False

        if action[0] == 'point':
            x, y = map(int, action[1:])
            self.draw_point(x, y)

        if action[0] == 'line':
            x0, y0, x1, y1 = map(int, action[1:])
            self.draw_line(x0, y0, x1, y1)


if __name__ == '__main__':
    PaintServer().run()
