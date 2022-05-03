import pygame
from config import *

class PaintBase:

    def __init__(self):
        self.is_running = False
        self.pygame_init()
        self.socket_init()

    def socket_init(self):
        pass

    def pygame_init(self):
        pygame.init()
        window_size = (WINDOW_WIDTH * PIXEL_SIZE, WINDOW_HEIGHT * PIXEL_SIZE)
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Paint')
        self.window.fill(COLOR_WHITE)
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                break

    def run(self):
        self.is_running = True
        while self.is_running:
            self.update()
            pygame.display.update()
        pygame.quit()