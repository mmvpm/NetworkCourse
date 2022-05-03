import pygame
import socket
from config import *
from paint_base import PaintBase

class PaintClient(PaintBase):

    def __init__(self):
        super().__init__()
        self.last_point = None
        self.mouse_pressed = False

    def socket_init(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)

    def send_action(self, action: str):
        self.socket.sendto(action.encode(), (HOST, PORT))
    
    def draw_point(self, x, y):
        if self.last_point is None:
            pygame.draw.circle(self.window, COLOR_BLACK, (x, y), BRUSH_THICKNESS)
            self.send_action(f'point {x} {y}')
        else:
            pygame.draw.line(self.window, COLOR_BLACK, self.last_point, (x, y), BRUSH_THICKNESS + 1)
            self.send_action(f'line {self.last_point[0]} {self.last_point[1]} {x} {y}')
        self.last_point = (x, y)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.send_action('quit')
                break
 
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                x, y = pygame.mouse.get_pos()
                self.draw_point(x, y)
 
            if event.type == pygame.MOUSEBUTTONUP:
                self.last_point = None
                self.mouse_pressed = False
 
            if event.type == pygame.MOUSEMOTION and self.mouse_pressed:
                x, y = pygame.mouse.get_pos()
                self.draw_point(x, y)

if __name__ == '__main__':
    PaintClient().run()
