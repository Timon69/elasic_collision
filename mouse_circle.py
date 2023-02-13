import pygame


class Mouse:
    def __init__(self, size: int):
        self.size = size

    def create_circle(self, mouse_coord: tuple):
        circle = pygame.rect.Rect(mouse_coord[0] - self.size // 2, mouse_coord[1] - self.size // 2, self.size, self.size)
        return circle
