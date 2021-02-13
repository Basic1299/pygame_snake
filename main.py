import pygame
import random
from SnakeHead import SnakeHead
from SnakeTail import SnakeTail
from Food import Food
from Score import Score
from Menu import Menu


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


def respawn_food():
    if pygame.sprite.groupcollide(food_group, snake_tail_group, False, False):
        for food_ in food_group:
            food_.kill()
        food_group.add(spawn_food())


def create_tail_part(snake_tail_id):
    snake_tail_id += 1
    if snake_tail_id == 1:
        new_tail = spawn_tail(snake_head, snake_tail_id, snake_head_group)
        first_tail_group.add(new_tail)
    else:
        new_tail = spawn_tail(snake_head, snake_tail_id, snake_tail_group)

    snake_tail_group.add(new_tail)
    snake_head.update_tail(len(snake_tail_group))

    return snake_tail_id


def out_of_screen():
    if snake_head.dir == "RIGHT":
        if snake_head.rect.right > SCREEN_WIDTH:
            return True
    elif snake_head.dir == "LEFT":
        if snake_head.rect.left < 0:
            return True
    elif snake_head.dir == "UP":
        if snake_head.rect.top < 0:
            return True
    elif snake_head.dir == "DOWN":
        if snake_head.rect.bottom > SCREEN_HEIGHT:
            return True

    return False


def head_tail_collision():
    if pygame.sprite.spritecollideany(snake_head, snake_tail_group):
        if not pygame.sprite.spritecollideany(snake_head, first_tail_group):
            return True

    return False


def is_game_over(state):
    if out_of_screen() or head_tail_collision():
        return "over"

    return state


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Game Variables
snake_tail_id = 0
current_time = 0
pressed_time = 0
snake_speed = 2 # [1, 2, 3, 4, 5]
bg_color = (0, 0, 0)
snake_color = "GREEN"
game_state = "player1_menu"

# Objects Initials
menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
score = Score()

# Sprite Groups
snake_head_group = pygame.sprite.Group()

first_tail_group = pygame.sprite.Group()
snake_tail_group = pygame.sprite.Group()

food = Food()

food_group = pygame.sprite.Group()
food_group.add(food)

# Fonts
title_font = pygame.font.SysFont("Arial", 64)
option_font = pygame.font.SysFont("Arial", 32)

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

                elif event.key == pygame.K_DOWN:
                    if menu.option < 2:
                        menu.option += 1

                if event.key == pygame.K_RETURN:
                    if menu.option == 0:
                        game_state = "player1_menu"
                        menu.option = 0

                    elif menu.option == 1:
                        menu.option = 0
                        pass

                    elif menu.option == 2:
                        pygame.quit()
                        exit()

        screen.fill(bg_color)

        # Title
        menu.draw_text(title_font, "S n a k e", (0, 255, 0), bg_color, (SCREEN_WIDTH//2, 80))

        # Options
        menu.draw_text(option_font, "One player", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 250))
        menu.draw_text(option_font, "Two players", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 300))
        menu.draw_text(option_font, "Exit", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 350))

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
                if event.key == pygame.K_ESCAPE:
                    run = False

                elif event.key == pygame.K_UP:
                    if menu.option > 0:
                        menu.option -= 1

                elif event.key == pygame.K_DOWN:
                    if menu.option < 4:
                        menu.option += 1

                if event.key == pygame.K_RETURN:
                    # Start
                    if menu.option == 3:
                        snake_head = SnakeHead(random.randint(30, SCREEN_WIDTH - 50),
                                               random.randint(30, SCREEN_HEIGHT - 50),
                                               snake_speed, snake_color)
                        snake_head_group.add(snake_head)
                        game_state = "player1_game"
                    # Back
                    elif menu.option == 4:
                        game_state = "main_menu"
                        menu.option = 0
                        menu.difficulty_option = 1
                        menu.color_option = 0

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

        screen.fill(bg_color)

        # Title
        menu.draw_text(title_font, "P l a y e r 1", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 80))

        # Options
        if menu.option != 0:
            menu.draw_text(option_font, "Name", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 250))

        if menu.option != 1:
            menu.draw_text(option_font, "Difficulty", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 300))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 76, 286, 157, 31), 2)

            if menu.difficulty_option == 0:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 287, 30, 30), 0)
            elif menu.difficulty_option == 1:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 45, 287, 30, 30), 0)
            elif menu.difficulty_option == 2:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 45, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 15, 287, 30, 30), 0)
            elif menu.difficulty_option == 3:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 45, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 15, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 15, 287, 30, 30), 0)
            elif menu.difficulty_option == 4:
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 75, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 45, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 15, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 15, 287, 30, 30), 0)
                pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 45, 287, 37, 30), 0)

        if menu.option != 2:
            menu.draw_text(option_font, "Skin color", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 350))
        else:
            # LEFT GREEN
            pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH//2 - 55, 337, 30, 30), 0)
            # MIDDLE RED
            pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH // 2 - 10, 337, 30, 30), 0)
            # RIGHT BLUE
            pygame.draw.rect(screen, (0, 0, 255), (SCREEN_WIDTH // 2 + 35, 337, 30, 30), 0)

        menu.draw_text(option_font, "Start", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 400))
        menu.draw_text(option_font, "Back", (0, 255, 0), bg_color, (SCREEN_WIDTH // 2, 500))

        # Draw borders
        # Name
        if menu.option == 0:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 232, (0, 255, 0))
            menu.is_color_option = False
            menu.is_difficulty_option = False
        # Difficulty
        elif menu.option == 1:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 282, (0, 255, 0))
            menu.is_difficulty_option = True
            menu.is_color_option = False
        # Color
        elif menu.option == 2:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 332, (0, 255, 0))
            menu.is_color_option = True
            menu.is_difficulty_option = False
        # Start
        elif menu.option == 3:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 382, (0, 255, 0))
            menu.is_color_option = False
            menu.is_difficulty_option = False
        # Back
        elif menu.option == 4:
            menu.draw_border(SCREEN_WIDTH // 2 - 92, 482, (0, 255, 0))
            menu.is_color_option = False
            menu.is_difficulty_option = False

        # Draw side borders
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

    # PLAYER 1 GAME
    elif game_state == "player1_game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                # Create two tails parts when movement keys pressed
                if snake_head.dir == "":
                    if event.key == pygame.K_RIGHT:
                        snake_head.dir = "RIGHT"
                        snake_tail_id = create_tail_part(snake_tail_id)
                        snake_head.create_eat_spot()

                    elif event.key == pygame.K_LEFT:
                        snake_head.dir = "LEFT"
                        snake_tail_id = create_tail_part(snake_tail_id)
                        snake_head.create_eat_spot()

                    elif event.key == pygame.K_UP:
                        snake_head.dir = "UP"
                        snake_tail_id = create_tail_part(snake_tail_id)
                        snake_head.create_eat_spot()

                    elif event.key == pygame.K_DOWN:
                        snake_head.dir = "DOWN"
                        snake_tail_id = create_tail_part(snake_tail_id)
                        snake_head.create_eat_spot()

                # Movement Keys
                if current_time - pressed_time > 150:
                    if event.key == pygame.K_LEFT and snake_head.dir != "RIGHT" and snake_head.dir != "LEFT":
                        snake_head.dir = "LEFT"
                        pressed_time = pygame.time.get_ticks()

                        if snake_head.tail_length > 0:
                            snake_head.create_new_dir_spot()

                    elif event.key == pygame.K_RIGHT and snake_head.dir != "LEFT" and snake_head.dir != "RIGHT":
                        snake_head.dir = "RIGHT"
                        pressed_time = pygame.time.get_ticks()

                        if snake_head.tail_length > 0:
                            snake_head.create_new_dir_spot()

                    elif event.key == pygame.K_UP and snake_head.dir != "DOWN" and snake_head.dir != "UP":
                        snake_head.dir = "UP"
                        pressed_time = pygame.time.get_ticks()

                        if snake_head.tail_length > 0:
                            snake_head.create_new_dir_spot()

                    elif event.key == pygame.K_DOWN and snake_head.dir != "UP" and snake_head.dir != "DOWN":
                        snake_head.dir = "DOWN"
                        pressed_time = pygame.time.get_ticks()

                        if snake_head.tail_length > 0:
                            snake_head.create_new_dir_spot()

                # Test
                if event.key == pygame.K_SPACE:
                    snake_tail_id += 1
                    if snake_tail_id == 1:
                        new_tail = spawn_tail(snake_head, snake_tail_id, snake_head_group)
                        first_tail_group.add(new_tail)
                    else:
                        new_tail = spawn_tail(snake_head, snake_tail_id, snake_tail_group)

                    snake_tail_group.add(new_tail)
                    snake_head.update_tail(len(snake_tail_group))

                # test
                if event.key == pygame.K_k:
                    game_state = "over"

        game_state = is_game_over(game_state)

        current_time = pygame.time.get_ticks()

        screen.fill(bg_color)

        # Respawn food spot if it spawns on the tail
        respawn_food()

        # Grow tail when eat spot reaches end of the snake
        if snake_head.spawn_tail:
            snake_head.spawn_tail = False
            snake_tail_id = create_tail_part(snake_tail_id)

        # Snake head and food collision
        if pygame.sprite.spritecollideany(snake_head, food_group):
            for food in food_group:
                food.kill()
            score.add_score(1)
            print(score.score)
            food_group.add(spawn_food())

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

        pygame.display.flip()

    elif game_state == "over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        option = input("play again? y/n: ")

        if option == "y":
            game_state = "player1_game"

            # Reset Variables
            snake_tail_id = 0
            current_time = 0
            pressed_time = 0

            score = Score()
            snake_head = SnakeHead(random.randint(30, SCREEN_WIDTH-50), random.randint(30, SCREEN_HEIGHT-50),
                                   snake_speed, snake_color)

            snake_head_group = pygame.sprite.Group()
            snake_head_group.add(snake_head)

            first_tail_group = pygame.sprite.Group()
            snake_tail_group = pygame.sprite.Group()

            food = Food()

            food_group = pygame.sprite.Group()
            food_group.add(food)

        else:
            run = False

pygame.quit()

















