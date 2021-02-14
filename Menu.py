import pygame


class Menu:
    def __init__(self, screen, sc_width, sc_height):
        self.screen = screen
        self.sc_width = sc_width
        self.sc_height = sc_height

        self.option = 0

        self.is_color_option = False
        self.is_difficulty_option = False
        self.is_wall_option = False

        self.color_option = 0
        self.difficulty_option = 1
        self.wall_option = 0

    def draw_text(self, font, text, text_color, center):
        text_image = font.render(f'{text}', True, text_color)
        text_rect = text_image.get_rect(center=center)
        self.screen.blit(text_image, text_rect)

    def draw_border(self, pos_x, pos_y, color):
        pygame.draw.rect(self.screen, color, (pos_x, pos_y, 190, 40), 1)



