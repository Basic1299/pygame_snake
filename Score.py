import pygame


class Score:
    def __init__(self, snake_head):
        self.snake_head = snake_head

        self.score = 0
        self.score_font = pygame.font.SysFont("Arial", 24)

    def add_score(self, number):
        self.score += number

    def draw_score(self, screen, position):
        score_image = self.score_font.render(f'{self.score}', True, self.set_color())
        score_rect = score_image.get_rect(center=position)
        screen.blit(score_image, score_rect)

    def set_color(self):
        if self.snake_head.snake_color == "GREEN":
            return 0, 255, 0
        elif self.snake_head.snake_color == "RED":
            return 255, 0, 0
        elif self.snake_head.snake_color == "BLUE":
            return 255, 255, 255

