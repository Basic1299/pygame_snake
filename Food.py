import pygame
import random


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coors = self.set_init_coors()
        self.color = self.set_random_color()
        self.size = (10, 10)

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.coors)

    def update(self):
        pass

    def set_random_color(self):
        R = random.randint(50, 200)
        G = random.randint(50, 200)
        B = random.randint(50, 200)

        return R, G, B

    def set_init_coors(self):
        x = random.randint(1, 779)
        y = random.randint(1, 579)

        return x, y
