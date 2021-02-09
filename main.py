import pygame
from SnakeHead import SnakeHead
from SnakeTail import SnakeTail


pygame.init()

def spawn_tail(head, num, preview_parts):
    for part in preview_parts:
        if num == 1:
            new_tail = SnakeTail(head, num, part)
        else:
            if part.id_number == num - 1:
                new_tail = SnakeTail(head, num, part)
    
    return new_tail

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Objects Inits
snake_head = SnakeHead(100, 100)

# Game Variables
snake_tail_id = 0
current_time = 0
pressed_time = 0

# Sprite Groups
snake_head_group = pygame.sprite.Group()
snake_head_group.add(snake_head)

snake_tail_group = pygame.sprite.Group()

# Game Loop
run = True
while run:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            # Movement Keys
            if event.key == pygame.K_LEFT and snake_head.dir != "RIGHT" and snake_head.dir != "LEFT":
                if current_time - pressed_time > 100:
                    pressed_time = pygame.time.get_ticks()
                    snake_head.dir = "LEFT"
                    if snake_head.tail_length > 0:
                        snake_head.coors_for_change_dir.append((snake_head.coors, snake_head.dir))

            elif event.key == pygame.K_RIGHT and snake_head.dir != "LEFT" and snake_head.dir != "RIGHT":
                if current_time - pressed_time > 100:
                    pressed_time = pygame.time.get_ticks()
                    snake_head.dir = "RIGHT"
                    if snake_head.tail_length > 0:
                        snake_head.coors_for_change_dir.append((snake_head.coors, snake_head.dir))

            elif event.key == pygame.K_UP and snake_head.dir != "DOWN" and snake_head.dir != "UP":
                if current_time - pressed_time > 100:
                    pressed_time = pygame.time.get_ticks()
                    snake_head.dir = "UP"
                    if snake_head.tail_length > 0:
                        snake_head.coors_for_change_dir.append((snake_head.coors, snake_head.dir))

            elif event.key == pygame.K_DOWN and snake_head.dir != "UP" and snake_head.dir != "DOWN":
                if current_time - pressed_time > 100:
                    pressed_time = pygame.time.get_ticks()
                    snake_head.dir = "DOWN"
                    if snake_head.tail_length > 0:
                        snake_head.coors_for_change_dir.append((snake_head.coors, snake_head.dir))

            # Test
            if event.key == pygame.K_SPACE:
                snake_tail_id += 1
                if snake_tail_id == 1:
                    new_tail = spawn_tail(snake_head, snake_tail_id, snake_head_group)
                else:
                    new_tail = spawn_tail(snake_head, snake_tail_id, snake_tail_group)
                    
                snake_tail_group.add(new_tail)
                snake_head.update_tail(len(snake_tail_group))
                
            # test
            if event.key == pygame.K_k:
                print("checks: " + str(len(snake_head.coors_for_change_dir)))
                print("times: " + str(len(snake_head.pressed_times)))
               
    current_time = pygame.time.get_ticks()
                    


    screen.fill((255, 255, 255))


    snake_head_group.update()
    snake_head_group.draw(screen)

    snake_tail_group.update()
    snake_tail_group.draw(screen)
    
        
    pygame.display.flip()

pygame.quit()

















