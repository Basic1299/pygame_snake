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

        self.current_time = pygame.time.get_ticks()
        self.initial_time = pygame.time.get_ticks()
        self.timer = random.choice([5_000, 7_500, 10_000, 12_500, 15_000])

    def update(self):
        self.update_time()
        self.respawn()

    def update_time(self):
        self.current_time = pygame.time.get_ticks()

    def respawn(self):
        if self.current_time - self.initial_time > self.timer:
            self.coors = self.set_init_coors()
            self.rect = self.image.get_rect(center=self.coors)
            self.initial_time = pygame.time.get_ticks()

    def set_random_color(self):
        chance = random.randint(0, 2)
        if chance == 0:
            return 255, 255, 255
        elif chance == 1:
            return 255, 255, 0
        elif chance == 2:
            return 0, 255, 0

    def set_init_coors(self):
        x = random.randint(10, 770)
        y = random.randint(10, 570)

        return x, y
