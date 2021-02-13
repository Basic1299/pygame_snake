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
        chance = random.randint(0, 2)
        if chance == 0:
            return 255, 255, 255
        elif chance == 1:
            return 255, 255, 0
        elif chance == 2:
            return 0, 255, 0

    def set_init_coors(self):
        x = random.randint(1, 779)
        y = random.randint(1, 579)

        return x, y
