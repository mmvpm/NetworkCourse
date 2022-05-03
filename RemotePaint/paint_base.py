import pygame
from config import *

class PaintBase:

    def __init__(self):
        self.is_running = False
        self.mouse_pressed = False
        self.last_point = None
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

    def draw_point(self, x, y):
        if self.last_point is None:
            pygame.draw.circle(self.window, COLOR_BLACK, (x, y), BRUSH_THICKNESS)
        else:
            pygame.draw.line(self.window, COLOR_BLACK, self.last_point, (x, y), BRUSH_THICKNESS + 1)
        self.last_point = (x, y)

    def update(self):
        pass

    def run(self):
        self.is_running = True
        while self.is_running:
            self.update()
            pygame.display.update()
        pygame.quit()