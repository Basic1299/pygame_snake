import pygame


class SnakeTail(pygame.sprite.Sprite):
    def __init__(self, snake_head, id_number, preview_part):
        super().__init__()
        self.snake_head = snake_head
        self.preview_part = preview_part
        self.id_number = id_number
        self.size = (20, 20)

        self.speed = snake_head.speed
        self.coors = self.set_spawn_position()
        self.color = self.set_color()
        
        self.init_dir = self.set_init_dir()
        self.dir = self.init_dir

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.coors)

        self.current_time = pygame.time.get_ticks()
        self.time_get = 0

    def update(self):
        self.position_update()
        self.dir_change()
        self.coors_for_dir_change_delete()
        self.spawn_tail_part()
        self.movement()
        self.color_change()
        self.time_update()

    def time_update(self):
        """Gets time in m seconds"""
        self.current_time = pygame.time.get_ticks()

    def set_init_dir(self):
        """Sets initial direction of a part based on the direction of a part in front of it"""
        if self.preview_part.dir == "RIGHT":
            return "RIGHT"
        elif self.preview_part.dir == "LEFT" :
            return "LEFT"
        elif self.preview_part.dir == "UP":
            return "UP"
        elif self.preview_part.dir == "DOWN":
            return "DOWN"

    def dir_change(self):
        """Changes direction based on a spot it collides"""
        for coors, direction in self.snake_head.coors_for_change_dir:
            if self.coors == coors and direction == "RIGHT":
                self.dir = "RIGHT"
            elif self.coors == coors and direction == "LEFT":
                self.dir = "LEFT"
            elif self.coors == coors and direction == "UP":
                self.dir = "UP"
            elif self.coors == coors and direction == "DOWN":
                self.dir = "DOWN"

    def coors_for_dir_change_delete(self):
        """Deletes a spot for direction changes when the last part of a tail collides it"""
        if len(self.snake_head.coors_for_change_dir) > 0:
            for coors, direction in self.snake_head.coors_for_change_dir:
                if self.coors == coors and self.id_number == self.snake_head.tail_length:
                    del self.snake_head.coors_for_change_dir[0]

    def position_update(self):
        """Updates coordinates"""
        self.coors = [self.rect.centerx, self.rect.centery]

    def spawn_tail_part(self):
        if len(self.snake_head.eat_spots) > 0:
            for coors in self.snake_head.eat_spots:
                if self.coors == coors and self.id_number == self.snake_head.tail_length:
                    self.snake_head.spawn_tail = True
                    del self.snake_head.eat_spots[0]

    def movement(self):
        """Moves the part based on its direction variable"""
        if self.dir == "RIGHT":
            self.rect.move_ip(self.speed, 0)
        elif self.dir == "LEFT":
            self.rect.move_ip(-self.speed, 0)
        elif self.dir == "UP":
            self.rect.move_ip(0, -self.speed)
        elif self.dir == "DOWN":
            self.rect.move_ip(0, self.speed)

    def set_spawn_position(self):
        """Sets spawn position based on the movement direction, id number and speed"""
        position = 20
        if self.id_number > 1:
            position = 18

        if self.speed == 3:
            position = 21
            if self.id_number > 1:
                position = 18

        elif self.speed == 4 or self.speed == 5:
            if self.id_number > 1:
                position = 20

        if self.preview_part.dir == "RIGHT":
            return [self.preview_part.coors[0]-position, self.preview_part.coors[1]]
        elif self.preview_part.dir == "LEFT":
            return [self.preview_part.coors[0]+position, self.preview_part.coors[1]]
        elif self.preview_part.dir == "UP":
            return [self.preview_part.coors[0], self.preview_part.coors[1]+position]
        elif self.preview_part.dir == "DOWN":
            return [self.preview_part.coors[0], self.preview_part.coors[1]-position]

    def color_change(self):
        """Changes color based on eaten food"""
        color = self.set_color()
        for spot_coors in self.snake_head.eat_spots:
            if self.coors == spot_coors:
                self.time_get = pygame.time.get_ticks()

        if self.current_time - self.time_get < 100:
            color = self.snake_head.head_color

        self.image.fill(color)

    def set_color(self):
        """Based on the head color sets colors of each tail part"""
        if self.snake_head.snake_color == "GREEN":
            if self.id_number % 2 == 0:
                return 0, 200, 0
            else:
                return 0, 255, 0

        elif self.snake_head.snake_color == "RED":
            if self.id_number % 2 == 0:
                return 200, 0, 0
            else:
                return 255, 0, 0

        elif self.snake_head.snake_color == "BLUE":
            if self.id_number % 2 == 0:
                return 0, 0, 200
            else:
                return 0, 0, 255






















