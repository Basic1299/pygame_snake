import pygame
import random
from SnakeHead import SnakeHead
from SnakeTail import SnakeTail
from Food import Food
from Score import Score
from Menu import Menu
from Brick import Brick
from HighScoresDatabase import HighScoresDB


pygame.init()


def spawn_tail(head, num, preview_parts):
    """Returns new tail part"""
    for part in preview_parts:
        if num == 1:
            new_tail = SnakeTail(head, num, part)
        else:
            if part.id_number == num - 1:
                new_tail = SnakeTail(head, num, part)
    
    return new_tail


def spawn_food():
    new_food = Food()
    return new_food


def respawn_food(tail_group):
    """Respawn food when it hits snakes tail or bricks during new init"""
    for food_ in food_group:
        if pygame.sprite.spritecollideany(food_, tail_group) or \
                pygame.sprite.spritecollideany(food_, brick_group):
            food_.kill()
            food_group.add(spawn_food())


def create_tail_part(tail_id, head, head_group, tail_group, first_tail_grp):
    tail_id += 1
    if tail_id == 1:
        new_tail = spawn_tail(head, tail_id, head_group)
        first_tail_grp.add(new_tail)
    else:
        new_tail = spawn_tail(head, tail_id, tail_group)

    tail_group.add(new_tail)
    head.update_tail(len(tail_group))

    return tail_id


def out_of_screen(head, transparency):
    """Based on transparency returns True when snake head is out of the screen or changes the head coors"""
    if not transparency:
        if head.dir == "RIGHT":
            if head.rect.right > SCREEN_WIDTH:
                return True
        elif head.dir == "LEFT":
            if head.rect.left < 0:
                return True
        elif head.dir == "UP":
            if head.rect.top < 0:
                return True
        elif head.dir == "DOWN":
            if head.rect.bottom > SCREEN_HEIGHT:
                return True
    else:
        if head.dir == "RIGHT":
            if head.rect.left > SCREEN_WIDTH:
                head.rect.centerx = 0
        elif head.dir == "LEFT":
            if head.rect.right < 0:
                head.rect.centerx = SCREEN_WIDTH
        elif head.dir == "UP":
            if head.rect.bottom < 0:
                head.rect.centery = SCREEN_HEIGHT
        elif head.dir == "DOWN":
            if head.rect.top > SCREEN_HEIGHT:
                head.rect.centery = 0

    return False


def head_tail_collision(head, tail_group, p_first_tail_group):
    """Return True if snake head hits its tail"""
    if pygame.sprite.spritecollideany(head, tail_group):
        if not pygame.sprite.spritecollideany(head, p_first_tail_group):
            return True

    return False


def p2_is_game_over(state, p1_head, p1_tail_group, p1_first_tail_group,
                    p2_head, p2_tail_group, p2_first_tail_group_,
                    p1_head_group, p2_head_group, transparency):
    """Checks every state what causes game over"""
    # Player 1
    if (out_of_screen(p1_head, transparency)
            or head_tail_collision(p1_head, p1_tail_group, p1_first_tail_group)
            or snake_head_bricks_collision(p1_head)
            or snake_snake_collision(p1_head, p2_head_group, p2_tail_group)):
        pygame.time.wait(3000)
        score.subtract_score(10)
        return "over"

    # Player 2
    if (out_of_screen(p2_head, transparency)
            or head_tail_collision(p2_head, p2_tail_group, p2_first_tail_group_)
            or snake_head_bricks_collision(p2_head)
            or snake_snake_collision(p2_head, p1_head_group, p1_tail_group)):
        pygame.time.wait(3000)
        p2_score.subtract_score(10)
        return "over"

    return state


def is_game_over(state, head, tail_group, first_tail_group_, transparency):
    """Checks every state what causes game over"""
    # Player 1
    if (out_of_screen(head, transparency)
            or head_tail_collision(head, tail_group, first_tail_group_)
            or snake_head_bricks_collision(head)):
        pygame.time.wait(3000)
        return "over"

    return state


def create_walls(h_walls_num, h_walls_len, v_walls_num, v_walls_len):
    """Based on number of walls and length of walls fill brick groups with walls"""
    start = 50
    width = 200

    # horizontal walls number
    hor_walls = random.randint(h_walls_num[0], h_walls_num[1])
    for j in range(hor_walls):
        pos_x = random.randint(start, width)
        pos_y = random.randint(start, width)

        # horizontal wall length
        hor_length = random.randint(h_walls_len[0], h_walls_len[1])
        for i in range(hor_length):
            brick_group.add(Brick(pos_x + i * 30, pos_y))

        start += 150
        width += 200

    start = 50
    width = 200

    # Vertical walls number
    ver_walls = random.randint(v_walls_num[0], v_walls_num[1])
    for j in range(ver_walls):
        pos_x = random.randint(start, width)
        pos_y = random.randint(start, width)

        # Vertical wall length
        ver_length = random.randint(v_walls_len[0], v_walls_len[1])
        for i in range(ver_length):
            brick_group.add(Brick(pos_x, pos_y + i * 30))

        start += 150
        width += 200


def create_brick_group(intensity):
    """Based on intensity creates brick group"""
    if intensity == 1:
        create_walls((1, 2), (2, 6), (1, 2), (2, 6))
    elif intensity == 2:
        create_walls((2, 3), (3, 6), (2, 3), (3, 6))
    elif intensity == 3:
        create_walls((3, 4), (4, 6), (3, 4), (4, 6))


def snake_head_init_brick_collision(head):
    """Returns True if snake head hits any brick during init"""
    if head.dir == "":
        if pygame.sprite.spritecollideany(head, brick_group):
            return True
    return False


def snake_head_bricks_collision(head):
    """Returns True if snake head hits any brick"""
    if pygame.sprite.spritecollideany(head, brick_group):
        return True
    return False


def snake_snake_collision(head, opposite_head_group, opposite_tail_group):
    """Returns True if snake head hits another player"""
    if (pygame.sprite.spritecollideany(head, opposite_head_group)
        or pygame.sprite.spritecollideany(head, opposite_tail_group)
        ):
        return True
    return False


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Arial", 64)
option_font = pygame.font.SysFont("Arial", 32)

# Game Variables
current_time = 0
pressed_time = 0
brick_intensity = 0
bg_color = (0, 0, 0)
game_state = "main_menu"
game_over_init = True
edge_transparency = True

# Player 1
snake_tail_id = 0
snake_speed = 2
snake_color = "GREEN"
menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

# Player 2
p2_snake_tail_id = 0
p2_snake_speed = 2
p2_snake_color = "GREEN"
p2_menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

# Objects Initials
high_score_db = HighScoresDB("high_score.db")

# Sprite Groups
# Player 1
snake_head_group = pygame.sprite.Group()
first_tail_group = pygame.sprite.Group()
snake_tail_group = pygame.sprite.Group()

# Player 2
p2_snake_head_group = pygame.sprite.Group()
p2_first_tail_group = pygame.sprite.Group()
p2_snake_tail_group = pygame.sprite.Group()

# Common
food_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()

# GAME STATES [main_menu, player1_menu, player1_game, player2_menu, player2_game, over]

# Game Loop
run = True
while run:
    clock.tick(60)
    # MAIN MENU
    if game_state == "main_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                elif event.key == pygame.K_UP:
                    if menu.option > 0:
                        menu.option -= 1

                    elif menu.option == 0:
                        menu.option = 2

                elif event.key == pygame.K_DOWN:
                    if menu.option < 2:
                        menu.option += 1

                    elif menu.option == 2:
                        menu.option = 0

                if event.key == pygame.K_RETURN:
                    # Player 1
                    if menu.option == 0:
                        game_state = "player1_menu"
                        menu.option = 0

                    # 2 players
                    elif menu.option == 1:
                        game_state = "player2_menu"
                        menu.option = 0

                    # Exit
                    elif menu.option == 2:
                        pygame.quit()
                        exit()

        if game_state == "main_menu":
            screen.fill(bg_color)

            # Title
            menu.draw_text(title_font, "S n a k e", (0, 255, 0), (SCREEN_WIDTH//2, 80))

            # Options
            menu.draw_text(option_font, "One player", (0, 255, 0), (SCREEN_WIDTH // 2, 250))
            menu.draw_text(option_font, "Two players", (0, 255, 0), (SCREEN_WIDTH // 2, 300))
            menu.draw_text(option_font, "Exit", (0, 255, 0), (SCREEN_WIDTH // 2, 350))

            # Draw borders
            if menu.option == 0:
                menu.draw_border(SCREEN_WIDTH // 2 - 92, 232, (0, 255, 0))
            elif menu.option == 1:
                menu.draw_border(SCREEN_WIDTH // 2 - 92, 282, (0, 255, 0))
            elif menu.option == 2:
                menu.draw_border(SCREEN_WIDTH // 2 - 92, 332, (0, 255, 0))

            pygame.display.flip()

    # PLAYER 1 MENU
    elif game_state == "player1_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Back
                if event.key == pygame.K_ESCAPE:
                    game_state = "main_menu"

                    # reset options
                    menu.option = 0
                    menu.difficulty_option = 1
                    menu.color_option = 0
                    menu.name = ""

                elif event.key == pygame.K_UP:
                    if menu.option > 0:
                        menu.option -= 1
                        menu.invalid_name = False

                    elif menu.option == 0:
                        menu.option = 5
                        menu.invalid_name = False

                elif event.key == pygame.K_DOWN:
                    if menu.option < 5:
                        menu.option += 1
                        menu.invalid_name = False

                    elif menu.option == 5:
                        menu.option = 0
                        menu.invalid_name = False

                if event.key == pygame.K_RETURN:
                    # Start
                    if menu.option == 4:
                        if len(menu.name) != 0:
                            menu.option = 0
                            create_brick_group(brick_intensity)

                            snake_head = SnakeHead(random.randint(30, SCREEN_WIDTH - 50),
                                                   random.randint(30, SCREEN_HEIGHT - 50),
                                                   snake_speed, snake_color, menu.name)
                            snake_head_group.add(snake_head)

                            food_group.add(spawn_food())

                            score = Score()
                            game_state = "player1_game"
                        else:
                            menu.invalid_name = True
                    # Back
                    elif menu.option == 5:
                        game_state = "main_menu"

                        # reset options
                        menu.option = 0
                        menu.difficulty_option = 1
                        menu.color_option = 0
                        menu.wall_option = 0
                        menu.name = ""

                # Side options colors
                if menu.is_color_option:
                    if event.key == pygame.K_LEFT:
                        if menu.color_option > 0:
                            menu.color_option -= 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.color_option < 2:
                            menu.color_option += 1

                # Side options difficulty
                if menu.is_difficulty_option:
                    if event.key == pygame.K_LEFT:
                        if menu.difficulty_option > 0:
                            menu.difficulty_option -= 1
                            snake_speed = menu.difficulty_option + 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.difficulty_option < 4:
                            menu.difficulty_option += 1
                            snake_speed = menu.difficulty_option + 1

                # Side options wall intensity
                if menu.is_wall_option:
                    if event.key == pygame.K_LEFT:
                        if menu.wall_option > 0:
                            menu.wall_option -= 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.wall_option < 3:
                            menu.wall_option += 1
                    brick_intensity = menu.wall_option

                # Name input
                if menu.is_name:
                    if event.key == pygame.K_BACKSPACE:
                        menu.name = menu.name[:-1]
                    else:
                        if menu.name.count("w") >= 3:
                            if len(menu.name) <= 7:
                                if (event.key != pygame.K_RETURN
                                        and event.key != pygame.K_SPACE
                                        and event.key != pygame.K_ESCAPE):
                                    menu.name += event.unicode
                        else:
                            if len(menu.name) <= 9:
                                if (event.key != pygame.K_RETURN
                                        and event.key != pygame.K_SPACE
                                        and event.key != pygame.K_ESCAPE):
                                    menu.name += event.unicode

        screen.fill(bg_color)

        # Title
        menu.draw_text(title_font, "O n e  P l a y e r", (0, 255, 0), (SCREEN_WIDTH // 2, 80))

        # Options
        # Name
        if menu.option != 0:
            if not menu.invalid_name:
                menu.draw_text(option_font, "Name", (0, 255, 0), (SCREEN_WIDTH // 2, 250))
            else:
                menu.draw_text(option_font, "Name", (255, 0, 0), (SCREEN_WIDTH // 2, 250))
            menu.is_name = False
        else:
            menu.is_name = True
            name_surf = option_font.render(menu.name, True, (255, 255, 255))
            screen.blit(name_surf, name_surf.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        # Speed
        if menu.option != 1:
            menu.draw_text(option_font, "Speed", (0, 255, 0), (SCREEN_WIDTH // 2, 300))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 76, 286, 157, 31), 2)

            if (
                menu.difficulty_option == 0
                or menu.difficulty_option == 1
                or menu.difficulty_option == 2
                or menu.difficulty_option == 3
                or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 287, 30, 30), 0)

            if (
                menu.difficulty_option == 1
                or menu.difficulty_option == 2
                or menu.difficulty_option == 3
                or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 45, 287, 30, 30), 0)

            if (
                menu.difficulty_option == 2
                or menu.difficulty_option == 3
                or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 15, 287, 30, 30), 0)

            if (
                menu.difficulty_option == 3
                or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 15, 287, 30, 30), 0)

            if menu.difficulty_option == 4:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 45, 287, 37, 30), 0)

        # Color
        if menu.option != 2:
            menu.draw_text(option_font, "Skin color", (0, 255, 0), (SCREEN_WIDTH // 2, 350))
        else:
            # LEFT GREEN
            pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH//2 - 55, 337, 30, 30), 0)
            # MIDDLE RED
            pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH // 2 - 10, 337, 30, 30), 0)
            # RIGHT BLUE
            pygame.draw.rect(screen, (0, 0, 255), (SCREEN_WIDTH // 2 + 35, 337, 30, 30), 0)

        # Wall intensity
        if menu.option != 3:
            menu.draw_text(option_font, "Wall intensity", (0, 255, 0), (SCREEN_WIDTH // 2, 400))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 76, 386, 157, 31), 2)

            if menu.wall_option == 1 or menu.wall_option == 2 or menu.wall_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 387, 50, 30), 0)
            if menu.wall_option == 2 or menu.wall_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 25, 387, 50, 30), 0)
            if menu.wall_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 25, 387, 55, 30), 0)

        # Start, Back
        menu.draw_text(option_font, "Start", (0, 255, 0), (SCREEN_WIDTH // 2, 450))
        menu.draw_text(option_font, "Back", (0, 255, 0), (SCREEN_WIDTH // 2, 500))

        # Draw borders
        # Name
        if menu.option == 0:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 232, (0, 255, 0))
            menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False
        # Difficulty
        elif menu.option == 1:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 282, (0, 255, 0))
            menu.is_difficulty_option = True
            menu.is_color_option = False
            menu.is_wall_option = False
        # Color
        elif menu.option == 2:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 332, (0, 255, 0))
            menu.is_color_option = True
            menu.is_difficulty_option = False
            menu.is_wall_option = False

        # Walls intensity
        elif menu.option == 3:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 382, (0, 255, 0))
            menu.is_wall_option = True
            menu.is_color_option = False
            menu.is_difficulty_option = False

        # Start
        elif menu.option == 4:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 432, (0, 255, 0))
            menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False
        # Back
        elif menu.option == 5:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 482, (0, 255, 0))
            menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False

        # Draw color side borders
        if menu.is_color_option:
            # GREEN
            if menu.color_option == 0:
                snake_color = "GREEN"
                pygame.draw.rect(screen, (0, 100, 0), (SCREEN_WIDTH // 2 - 50, 342, 20, 20), 0)
            # RED
            elif menu.color_option == 1:
                snake_color = "RED"
                pygame.draw.rect(screen, (100, 0, 0), (SCREEN_WIDTH // 2 - 5, 342, 20, 20), 0)
            # BLUE
            elif menu.color_option == 2:
                snake_color = "BLUE"
                pygame.draw.rect(screen, (0, 0, 100), (SCREEN_WIDTH // 2 + 40, 342, 20, 20), 0)

        pygame.display.flip()

    # PLAYER 2 MENU
    elif game_state == "player2_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Back
                if event.key == pygame.K_ESCAPE:
                    game_state = "main_menu"

                    # reset options
                    menu.option = 0
                    menu.difficulty_option = 1
                    menu.color_option = 0
                    menu.wall_option = 0
                    menu.name = ""

                    p2_menu.color_option = 0
                    p2_menu.name = ""

                if event.key == pygame.K_UP:
                    if menu.option > 0:
                        menu.option -= 1
                        menu.invalid_name = False
                        p2_menu.invalid_name = False

                    elif menu.option == 0:
                        menu.option = 7
                        menu.invalid_name = False
                        p2_menu.invalid_name = False

                elif event.key == pygame.K_DOWN:
                    if menu.option < 7:
                        menu.option += 1
                        menu.invalid_name = False
                        p2_menu.invalid_name = False

                    elif menu.option == 7:
                        menu.option = 0
                        menu.invalid_name = False
                        p2_menu.invalid_name = False

                if event.key == pygame.K_RETURN:
                    # Start
                    if menu.option == 6:
                        if len(menu.name) != 0 and len(p2_menu.name) != 0:
                            menu.option = 0
                            create_brick_group(brick_intensity)

                            # Spawn 2 foods
                            food_group.add(spawn_food(), spawn_food())

                            # Player 1 initial
                            snake_head = SnakeHead(random.randint(30, SCREEN_WIDTH - 50),
                                                   random.randint(30, SCREEN_HEIGHT - 50),
                                                   snake_speed, snake_color, menu.name)
                            snake_head_group.add(snake_head)
                            score = Score()

                            # Player 2 initial
                            p2_snake_head = SnakeHead(random.randint(30, SCREEN_WIDTH - 50),
                                                      random.randint(30, SCREEN_HEIGHT - 50),
                                                      p2_snake_speed, p2_snake_color, p2_menu.name)
                            p2_snake_head_group.add(p2_snake_head)
                            p2_score = Score()

                            game_state = "player2_game"
                        else:
                            if len(menu.name) == 0:
                                menu.invalid_name = True
                            if len(p2_menu.name) == 0:
                                p2_menu.invalid_name = True

                    # Back
                    if menu.option == 7:
                        game_state = "main_menu"

                        # reset options
                        menu.option = 0
                        menu.difficulty_option = 1
                        menu.color_option = 0
                        menu.name = ""

                        p2_menu.color_option = 0
                        p2_menu.name = ""

                # Side options difficulty
                if menu.is_difficulty_option:
                    if event.key == pygame.K_LEFT:
                        if menu.difficulty_option > 0:
                            menu.difficulty_option -= 1
                            snake_speed = menu.difficulty_option + 1
                            p2_snake_speed = menu.difficulty_option + 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.difficulty_option < 4:
                            menu.difficulty_option += 1
                            snake_speed = menu.difficulty_option + 1
                            p2_snake_speed = menu.difficulty_option + 1

                # Side options wall intensity
                if menu.is_wall_option:
                    if event.key == pygame.K_LEFT:
                        if menu.wall_option > 0:
                            menu.wall_option -= 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.wall_option < 3:
                            menu.wall_option += 1
                    brick_intensity = menu.wall_option

                # Name input
                # Player 1
                if menu.is_name:
                    if event.key == pygame.K_BACKSPACE:
                        menu.name = menu.name[:-1]
                    else:
                        if menu.name.count("w") >= 3:
                            if len(menu.name) <= 7:
                                if (event.key != pygame.K_RETURN
                                        and event.key != pygame.K_SPACE
                                        and event.key != pygame.K_ESCAPE):
                                    menu.name += event.unicode
                        else:
                            if len(menu.name) <= 9:
                                if (event.key != pygame.K_RETURN
                                        and event.key != pygame.K_SPACE
                                        and event.key != pygame.K_ESCAPE):
                                    menu.name += event.unicode

                # Side options colors
                # Player 1
                if menu.is_color_option:
                    if event.key == pygame.K_LEFT:
                        if menu.color_option > 0:
                            menu.color_option -= 1
                    elif event.key == pygame.K_RIGHT:
                        if menu.color_option < 2:
                            menu.color_option += 1

                # Name input
                # Player 2
                if p2_menu.is_name:
                    if event.key == pygame.K_BACKSPACE:
                        p2_menu.name = p2_menu.name[:-1]
                    else:
                        if p2_menu.name.count("w") >= 3:
                            if len(p2_menu.name) <= 7:
                                if (event.key != pygame.K_RETURN
                                        and event.key != pygame.K_SPACE
                                        and event.key != pygame.K_ESCAPE):
                                    p2_menu.name += event.unicode
                        else:
                            if len(p2_menu.name) <= 9:
                                if (event.key != pygame.K_RETURN
                                        and event.key != pygame.K_SPACE
                                        and event.key != pygame.K_ESCAPE):
                                    p2_menu.name += event.unicode

                # Side options colors
                # Player 2
                if p2_menu.is_color_option:
                    if event.key == pygame.K_LEFT:
                        if p2_menu.color_option > 0:
                            p2_menu.color_option -= 1
                    elif event.key == pygame.K_RIGHT:
                        if p2_menu.color_option < 2:
                            p2_menu.color_option += 1

        screen.fill(bg_color)

        # Title
        menu.draw_text(title_font, "T w o  P l a y e r s", (0, 255, 0), (SCREEN_WIDTH // 2, 80))

        # OPTIONS
        # player 1
        # Name
        if menu.option != 0:
            if not menu.invalid_name:
                menu.draw_text(option_font, "Player 1", (0, 255, 0), (250, 200))
            else:
                menu.draw_text(option_font, "Player 1", (255, 0, 0), (250, 200))
        else:
            name_surf = option_font.render(menu.name, True, (255, 255, 255))
            screen.blit(name_surf, name_surf.get_rect(center=(250, 200)))

        # Color
        if menu.option != 1:
            menu.draw_text(option_font, "Skin color", (0, 255, 0), (250, 250))
        else:
            # LEFT GREEN
            pygame.draw.rect(screen, (0, 255, 0), (185, 235, 30, 30), 0)
            # MIDDLE RED
            pygame.draw.rect(screen, (255, 0, 0), (230, 235, 30, 30), 0)
            # RIGHT BLUE
            pygame.draw.rect(screen, (0, 0, 255), (275, 235, 30, 30), 0)

        # Player 2
        if menu.option != 2:
            if not p2_menu.invalid_name:
                p2_menu.draw_text(option_font, "Player 2", (0, 255, 0), (550, 200))
            else:
                p2_menu.draw_text(option_font, "Player 2", (255, 0, 0), (550, 200))
        else:
            name_surf = option_font.render(p2_menu.name, True, (255, 255, 255))
            screen.blit(name_surf, name_surf.get_rect(center=(550, 200)))

        # Color
        if menu.option != 3:
            p2_menu.draw_text(option_font, "Skin color", (0, 255, 0), (550, 250))
        else:
            # LEFT GREEN
            pygame.draw.rect(screen, (0, 255, 0), (485, 235, 30, 30), 0)
            # MIDDLE RED
            pygame.draw.rect(screen, (255, 0, 0), (530, 235, 30, 30), 0)
            # RIGHT BLUE
            pygame.draw.rect(screen, (0, 0, 255), (575, 235, 30, 30), 0)

        # Common
        # Speed
        if menu.option != 4:
            menu.draw_text(option_font, "Speed", (0, 255, 0), (SCREEN_WIDTH // 2, 350))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 76, 334, 157, 31), 2)

            if (
                    menu.difficulty_option == 0
                    or menu.difficulty_option == 1
                    or menu.difficulty_option == 2
                    or menu.difficulty_option == 3
                    or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 334, 30, 30), 0)

            if (
                    menu.difficulty_option == 1
                    or menu.difficulty_option == 2
                    or menu.difficulty_option == 3
                    or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 45, 334, 30, 30), 0)

            if (
                    menu.difficulty_option == 2
                    or menu.difficulty_option == 3
                    or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 15, 334, 30, 30), 0)

            if (
                    menu.difficulty_option == 3
                    or menu.difficulty_option == 4
            ):
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 15, 334, 30, 30), 0)

            if menu.difficulty_option == 4:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 45, 334, 37, 30), 0)

        # Wall Intensity
        if menu.option != 5:
            menu.draw_text(option_font, "Wall intensity", (0, 255, 0), (SCREEN_WIDTH // 2, 400))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 76, 384, 157, 31), 2)

            if menu.wall_option == 1 or menu.wall_option == 2 or menu.wall_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 384, 50, 30), 0)
            if menu.wall_option == 2 or menu.wall_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 25, 384, 50, 30), 0)
            if menu.wall_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 25, 384, 55, 30), 0)

        # Start, Back
        menu.draw_text(option_font, "Start", (0, 255, 0), (SCREEN_WIDTH // 2, 500))
        menu.draw_text(option_font, "Back", (0, 255, 0), (SCREEN_WIDTH // 2, 550))

        # DRAW BORDERS
        # player 1
        # Name
        if menu.option == 0:
            menu.draw_border(152, 180, (0, 255, 0))
            menu.is_name = True
            menu.is_color_option = False
            p2_menu.is_name = False
            p2_menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False

        # Color
        elif menu.option == 1:
            menu.draw_border(152, 230, (0, 255, 0))
            menu.is_color_option = True
            menu.is_name = False
            p2_menu.is_name = False
            p2_menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False

        # player 2
        # Name
        elif menu.option == 2:
            menu.draw_border(452, 180, (0, 255, 0))
            p2_menu.is_name = True
            p2_menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False
            menu.is_color_option = False
            menu.is_name = False
        # Color
        elif menu.option == 3:
            menu.draw_border(452, 230, (0, 255, 0))
            p2_menu.is_color_option = True
            p2_menu.is_name = False
            menu.is_color_option = False
            menu.is_difficulty_option = False
            menu.is_wall_option = False
            menu.is_name = False

        # Common
        # Speed
        elif menu.option == 4:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 330, (0, 255, 0))
            menu.is_difficulty_option = True
            menu.is_wall_option = False
            menu.is_name = False
            p2_menu.is_color_option = False
            p2_menu.is_name = False
            p2_menu.is_color_option = False
        # Wall intensity
        elif menu.option == 5:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 380, (0, 255, 0))
            menu.is_wall_option = True
            menu.is_name = False
            p2_menu.is_color_option = False
            p2_menu.is_name = False
            p2_menu.is_color_option = False
            menu.is_difficulty_option = False

        # Start
        elif menu.option == 6:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 480, (0, 255, 0))
        # Back
        elif menu.option == 7:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 530, (0, 255, 0))

        # Draw color side borders
        # Player 1
        if menu.is_color_option:
            # GREEN
            if menu.color_option == 0:
                snake_color = "GREEN"
                pygame.draw.rect(screen, (0, 100, 0), (190, 240, 20, 20), 0)
            # RED
            elif menu.color_option == 1:
                snake_color = "RED"
                pygame.draw.rect(screen, (100, 0, 0), (235, 240, 20, 20), 0)
            # BLUE
            elif menu.color_option == 2:
                snake_color = "BLUE"
                pygame.draw.rect(screen, (0, 0, 100), (280, 240, 20, 20), 0)

        # Player 2
        if p2_menu.is_color_option:
            # GREEN
            if p2_menu.color_option == 0:
                p2_snake_color = "GREEN"
                pygame.draw.rect(screen, (0, 100, 0), (490, 240, 20, 20), 0)
            # RED
            elif p2_menu.color_option == 1:
                p2_snake_color = "RED"
                pygame.draw.rect(screen, (100, 0, 0), (535, 240, 20, 20), 0)
            # BLUE
            elif p2_menu.color_option == 2:
                p2_snake_color = "BLUE"
                pygame.draw.rect(screen, (0, 0, 100), (580, 240, 20, 20), 0)

        pygame.display.flip()

    # PLAYER 1 GAME
    elif game_state == "player1_game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Reset and back to the menu
                if event.key == pygame.K_ESCAPE:
                    game_state = "main_menu"
                    # Reset Variables
                    brick_intensity = 0
                    current_time = 0
                    pressed_time = 0
                    game_over_init = True

                    # Player 1
                    snake_speed = 2
                    snake_tail_id = 0
                    snake_color = "GREEN"

                    # Objects and sprite groups deletes, empties
                    food_group.empty()

                    # Player 1
                    del snake_head
                    snake_head_group.empty()

                    first_tail_group.empty()
                    snake_tail_group.empty()
                    brick_group.empty()

                    del menu
                    menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

                    del score

                # Create two tails parts when movement keys pressed
                if game_state == "player1_game":
                    if snake_head.dir == "":
                        if event.key == pygame.K_RIGHT:
                            snake_head.dir = "RIGHT"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                        elif event.key == pygame.K_LEFT:
                            snake_head.dir = "LEFT"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                        elif event.key == pygame.K_UP:
                            snake_head.dir = "UP"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                        elif event.key == pygame.K_DOWN:
                            snake_head.dir = "DOWN"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                # Movement Keys
                if game_state == "player1_game":
                    if snake_head.distance_between == 0:
                        if event.key == pygame.K_LEFT and snake_head.dir != "RIGHT" and snake_head.dir != "LEFT":
                            snake_head.dir = "LEFT"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_RIGHT and snake_head.dir != "LEFT" and snake_head.dir != "RIGHT":
                            snake_head.dir = "RIGHT"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_UP and snake_head.dir != "DOWN" and snake_head.dir != "UP":
                            snake_head.dir = "UP"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_DOWN and snake_head.dir != "UP" and snake_head.dir != "DOWN":
                            snake_head.dir = "DOWN"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

        # Respawn snake head if it collides bricks on the spawn
        if game_state == "player1_game":
            while snake_head_init_brick_collision(snake_head):
                snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

            game_state = is_game_over(game_state, snake_head,
                                      snake_tail_group, first_tail_group,
                                      edge_transparency)

            current_time = pygame.time.get_ticks()

            screen.fill(bg_color)

            # Respawn food spot if it spawns on the tail or bricks
            respawn_food(snake_tail_group)

            # Grow tail when eat spot reaches end of the snake
            if snake_head.spawn_tail:
                snake_head.spawn_tail = False
                snake_tail_id = create_tail_part(snake_tail_id, snake_head,
                                                 snake_head_group, snake_tail_group,
                                                 first_tail_group)

            # Snake head and food collision
            for food in food_group:
                if pygame.sprite.collide_rect(snake_head, food):
                    food.kill()
                    score.add_score(1)
                    food = spawn_food()
                    food_group.add(food)

                    if snake_head.tail_length > 0:
                        snake_head.create_eat_spot()
                    else:
                        snake_head.spawn_tail = True

            # Drawing
            food_group.update()
            food_group.draw(screen)

            snake_tail_group.update()
            snake_tail_group.draw(screen)

            snake_head_group.update()
            snake_head_group.draw(screen)

            brick_group.draw(screen)

            score.draw_score(screen, (15, 15), snake_head.snake_color)

            pygame.display.flip()

    # 2 PLAYERS GAME
    elif game_state == "player2_game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Reset and back to the main menu
                if event.key == pygame.K_ESCAPE:
                    game_state = "main_menu"

                    # Reset Variables
                    brick_intensity = 0
                    current_time = 0
                    pressed_time = 0
                    game_over_init = True

                    # Player 1
                    snake_speed = 2
                    snake_tail_id = 0
                    snake_color = "GREEN"

                    # Objects and sprite groups deletes, empties
                    food_group.empty()

                    # Player 1
                    del snake_head
                    snake_head_group.empty()

                    first_tail_group.empty()
                    snake_tail_group.empty()
                    brick_group.empty()

                    del menu
                    menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

                    del score

                    # Player 2
                    if len(p2_snake_head_group) > 0:
                        p2_snake_speed = 2
                        p2_snake_tail_id = 0
                        p2_snake_color = "GREEN"

                        # Objects and sprite groups deletes, empties
                        del p2_snake_head
                        p2_snake_head_group.empty()

                        p2_first_tail_group.empty()
                        p2_snake_tail_group.empty()

                        del p2_menu
                        p2_menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

                        del p2_score

                # Create two tails parts when movement keys pressed
                # Player 1
                if game_state == "player2_game":
                    if snake_head.dir == "":
                        if event.key == pygame.K_RIGHT:
                            snake_head.dir = "RIGHT"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                        elif event.key == pygame.K_LEFT:
                            snake_head.dir = "LEFT"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                        elif event.key == pygame.K_UP:
                            snake_head.dir = "UP"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                        elif event.key == pygame.K_DOWN:
                            snake_head.dir = "DOWN"
                            snake_tail_id = create_tail_part(snake_tail_id, snake_head, snake_head_group,
                                                             snake_tail_group, first_tail_group)
                            snake_head.create_eat_spot()

                    # Create two tails parts when movement keys pressed
                    # Player 2
                    if p2_snake_head.dir == "":
                        if event.key == pygame.K_d:
                            p2_snake_head.dir = "RIGHT"
                            p2_snake_tail_id = create_tail_part(p2_snake_tail_id, p2_snake_head, p2_snake_head_group,
                                                                p2_snake_tail_group, p2_first_tail_group)
                            p2_snake_head.create_eat_spot()

                        elif event.key == pygame.K_a:
                            p2_snake_head.dir = "LEFT"
                            p2_snake_tail_id = create_tail_part(p2_snake_tail_id, p2_snake_head, p2_snake_head_group,
                                                                p2_snake_tail_group, p2_first_tail_group)
                            p2_snake_head.create_eat_spot()

                        elif event.key == pygame.K_w:
                            p2_snake_head.dir = "UP"
                            p2_snake_tail_id = create_tail_part(p2_snake_tail_id, p2_snake_head, p2_snake_head_group,
                                                                p2_snake_tail_group, p2_first_tail_group)
                            p2_snake_head.create_eat_spot()

                        elif event.key == pygame.K_s:
                            p2_snake_head.dir = "DOWN"
                            p2_snake_tail_id = create_tail_part(p2_snake_tail_id, p2_snake_head, p2_snake_head_group,
                                                                p2_snake_tail_group, p2_first_tail_group)
                            p2_snake_head.create_eat_spot()

                # Movement Keys
                # Player 1
                if game_state == "player2_game":
                    if snake_head.distance_between == 0:
                        if event.key == pygame.K_LEFT and snake_head.dir != "RIGHT" and snake_head.dir != "LEFT":
                            snake_head.dir = "LEFT"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_RIGHT and snake_head.dir != "LEFT" and snake_head.dir != "RIGHT":
                            snake_head.dir = "RIGHT"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_UP and snake_head.dir != "DOWN" and snake_head.dir != "UP":
                            snake_head.dir = "UP"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_DOWN and snake_head.dir != "UP" and snake_head.dir != "DOWN":
                            snake_head.dir = "DOWN"

                            if snake_head.tail_length > 0:
                                snake_head.create_new_dir_spot()

                    # Movement Keys
                    # Player 2
                    if p2_snake_head.distance_between == 0:
                        if event.key == pygame.K_a and p2_snake_head.dir != "RIGHT" and p2_snake_head.dir != "LEFT":
                            p2_snake_head.dir = "LEFT"

                            if p2_snake_head.tail_length > 0:
                                p2_snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_d and p2_snake_head.dir != "LEFT" and p2_snake_head.dir != "RIGHT":
                            p2_snake_head.dir = "RIGHT"

                            if p2_snake_head.tail_length > 0:
                                p2_snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_w and p2_snake_head.dir != "DOWN" and p2_snake_head.dir != "UP":
                            p2_snake_head.dir = "UP"

                            if p2_snake_head.tail_length > 0:
                                p2_snake_head.create_new_dir_spot()

                        elif event.key == pygame.K_s and p2_snake_head.dir != "UP" and p2_snake_head.dir != "DOWN":
                            p2_snake_head.dir = "DOWN"

                            if p2_snake_head.tail_length > 0:
                                p2_snake_head.create_new_dir_spot()

        # Respawn snake head if it collides bricks on the spawn
        # Player 1
        if game_state == "player2_game":
            while snake_head_init_brick_collision(snake_head):
                snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

            # Respawn snake head if it collides bricks on the spawn
            # Player 2
            while snake_head_init_brick_collision(p2_snake_head):
                p2_snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                p2_snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

            # Respawn players if they collide on the on the beginning with each other
            # Both Players
            while (snake_snake_collision(snake_head, p2_snake_head_group, p2_snake_tail_group)
                    and snake_head.dir == ""
                    and p2_snake_head.dir == ""):
                snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

                p2_snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                p2_snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

            game_state = p2_is_game_over(game_state, snake_head, snake_tail_group, first_tail_group,
                                         p2_snake_head, p2_snake_tail_group, p2_first_tail_group,
                                         snake_head_group, p2_snake_head_group, edge_transparency)

            current_time = pygame.time.get_ticks()

            screen.fill(bg_color)

            # Respawn food spot if it spawns on the tail or bricks
            # Player 1
            respawn_food(snake_tail_group)
            # Player 2
            respawn_food(p2_snake_tail_group)

            # Grow tail when eat spot reaches end of the snake
            # Player 1
            if snake_head.spawn_tail:
                snake_head.spawn_tail = False
                snake_tail_id = create_tail_part(snake_tail_id, snake_head,
                                                 snake_head_group, snake_tail_group,
                                                 first_tail_group)

            # Player 2
            if p2_snake_head.spawn_tail:
                p2_snake_head.spawn_tail = False
                p2_snake_tail_id = create_tail_part(p2_snake_tail_id, p2_snake_head,
                                                    p2_snake_head_group, p2_snake_tail_group,
                                                    p2_first_tail_group)

            # Snake head and food collision
            # Player 1
            for food in food_group:
                if pygame.sprite.collide_rect(snake_head, food):
                    food.kill()
                    score.add_score(1)
                    food = spawn_food()
                    food_group.add(food)

                    if snake_head.tail_length > 0:
                        snake_head.create_eat_spot()
                    else:
                        snake_head.spawn_tail = True

            # Snake head and food collision
            # Player 1
            for food in food_group:
                if pygame.sprite.collide_rect(p2_snake_head, food):
                    food.kill()
                    p2_score.add_score(1)
                    food = spawn_food()
                    food_group.add(food)

                    if p2_snake_head.tail_length > 0:
                        p2_snake_head.create_eat_spot()
                    else:
                        p2_snake_head.spawn_tail = True

            # Drawing
            food_group.update()
            food_group.draw(screen)

            # Player 1
            snake_tail_group.update()
            snake_tail_group.draw(screen)

            snake_head_group.update()
            snake_head_group.draw(screen)

            score.draw_score(screen, (15, 15), snake_head.snake_color)

            # Player 2
            p2_snake_tail_group.update()
            p2_snake_tail_group.draw(screen)

            p2_snake_head_group.update()
            p2_snake_head_group.draw(screen)

            brick_group.draw(screen)

            p2_score.draw_score(screen, (770, 15), p2_snake_head.snake_color)

            pygame.display.flip()

    elif game_state == "over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_RETURN:
                    # Play again
                    if menu.option == 0:
                        if len(p2_snake_head_group) > 0:
                            game_state = "player2_game"
                            p2_snake_tail_id = 0
                            p2_snake_head.dir = ""
                            p2_snake_head.tail_length = 0

                            p2_snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                            p2_snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

                            p2_snake_head.coors_for_change_dir.clear()
                            p2_snake_head.eat_spots.clear()
                            p2_snake_head.spawn_tail = False
                            p2_snake_head.tail_length = 0
                            p2_snake_tail_group.empty()
                            p2_first_tail_group.empty()
                            p2_score.score = 0
                        else:
                            game_state = "player1_game"

                        # Reset Variables
                        # Player 1
                        snake_tail_id = 0
                        current_time = 0
                        pressed_time = 0

                        snake_head.dir = ""
                        snake_head.tail_length = 0

                        snake_head.rect.centerx = random.randint(30, SCREEN_WIDTH - 50)
                        snake_head.rect.centery = random.randint(30, SCREEN_HEIGHT - 50)

                        snake_head.coors_for_change_dir.clear()
                        snake_head.eat_spots.clear()
                        snake_head.spawn_tail = False
                        snake_head.tail_length = 0
                        snake_tail_group.empty()
                        first_tail_group.empty()
                        score.score = 0

                        game_over_init = True

                    # Back to menu
                    else:
                        game_state = "main_menu"

                        # Reset Variables
                        brick_intensity = 0
                        current_time = 0
                        pressed_time = 0
                        game_over_init = True

                        # Player 1
                        snake_speed = 2
                        snake_tail_id = 0
                        snake_color = "GREEN"

                        # Objects and sprite groups deletes, empties
                        food_group.empty()

                        # Player 1
                        del snake_head
                        snake_head_group.empty()

                        first_tail_group.empty()
                        snake_tail_group.empty()
                        brick_group.empty()

                        del menu
                        menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

                        del score

                        # Player 2
                        if len(p2_snake_head_group) > 0:
                            p2_snake_speed = 2
                            p2_snake_tail_id = 0
                            p2_snake_color = "GREEN"

                            # Objects and sprite groups deletes, empties
                            del p2_snake_head
                            p2_snake_head_group.empty()

                            p2_first_tail_group.empty()
                            p2_snake_tail_group.empty()

                            del p2_menu
                            p2_menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

                            del p2_score

                # Move between buttons
                elif event.key == pygame.K_UP:
                    if menu.option > 0:
                        menu.option -= 1

                    elif menu.option == 0:
                        menu.option = 1

                elif event.key == pygame.K_DOWN:
                    if menu.option < 1:
                        menu.option += 1

                    elif menu.option == 1:
                        menu.option = 0

        if game_state == "over":
            # Add score to the database
            if game_over_init:
                game_over_init = False
                # Player 1
                high_score_db.add_record(snake_head.name, score.score)

                # Player 2
                if len(p2_snake_head_group) > 0:
                    high_score_db.add_record(p2_snake_head.name, p2_score.score)

            screen.fill(bg_color)

            # title
            menu.draw_text(title_font, "H i g h  S c o r e", (0, 255, 0), (SCREEN_WIDTH // 2, 80))

            # Score Table
            high_score_db.draw_table(option_font, screen)

            # Draw Buttons
            menu.draw_text(option_font, "Play again", (0, 255, 0), (SCREEN_WIDTH // 2, 500))
            menu.draw_text(option_font, "Menu", (0, 255, 0), (SCREEN_WIDTH // 2, 550))

            # Draw borders
            if menu.option == 0:
                menu.draw_border(SCREEN_WIDTH // 2 - 92, 482, (0, 255, 0))
            elif menu.option == 1:
                menu.draw_border(SCREEN_WIDTH // 2 - 92, 532, (0, 255, 0))

            pygame.display.flip()

pygame.quit()
