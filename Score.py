import pygame


class Score:
    def __init__(self):
        self.score = 0
        self.score_font = pygame.font.SysFont("Arial", 24)

    def add_score(self, number):
        self.score += number

    def draw_score(self, screen, position, color):
        score_image = self.score_font.render(f'{self.score}', True, color)
        score_rect = score_image.get_rect(center=position)
        screen.blit(score_image, score_rect)



