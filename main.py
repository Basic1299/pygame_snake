import pygame
from SnakeHead import SnakeHead
from SnakeTail import SnakeTail
from Food import Food
from Score import Score


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


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Game Variables
snake_tail_id = 0
current_time = 0
pressed_time = 0
game_speed = 250

# Objects Initials
score = Score()
snake_head = SnakeHead(100, 100)

# Sprite Groups
snake_head_group = pygame.sprite.Group()
snake_head_group.add(snake_head)

first_tail_group = pygame.sprite.Group()
snake_tail_group = pygame.sprite.Group()

food = Food()

food_group = pygame.sprite.Group()
food_group.add(food)


# Game Loop
run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

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
                pass

    current_time = pygame.time.get_ticks()

    screen.fill((255, 255, 255))

    # Respawn food spot if it spawns on the tail
    respawn_food()

    # Collision between head and tail
    if pygame.sprite.spritecollideany(snake_head, snake_tail_group):
        if not pygame.sprite.spritecollideany(snake_head, first_tail_group):
            print("collision")

    # Grow tail when eat spot reaches end of the snake
    if snake_head.spawn_tail:
        snake_head.spawn_tail = False
        snake_tail_id += 1
        if snake_tail_id == 1:
            new_tail = spawn_tail(snake_head, snake_tail_id, snake_head_group)
            first_tail_group.add(new_tail)
        else:
            new_tail = spawn_tail(snake_head, snake_tail_id, snake_tail_group)

        snake_tail_group.add(new_tail)
        snake_head.update_tail(len(snake_tail_group))

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

pygame.quit()

















