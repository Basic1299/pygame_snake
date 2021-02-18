import random
import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.size = (30, 30)
        self.color = (150, 150, 150)

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def set_size(self):
        number = random.randint(20, 30)
        return number, number

    def get_position(self):
        x = random.randint(0, 770)
        y = random.randint(0, 570)
        return x, y
