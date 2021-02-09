import pygame

class SnakeTail(pygame.sprite.Sprite):
    def __init__(self, snake_head, id_number, preview_part):
        super().__init__()
        self.snake_head = snake_head
        self.preview_part = preview_part
        self.id_number = id_number
        self.size = (20, 20)
        self.coors = self.set_spawn_position()
        self.color = (0, 255, 0)
        
        self.init_dir = self.set_init_dir()
        self.dir = self.init_dir
        self.speed = snake_head.speed

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.coors)

    def update(self):
        self.position_update()
        self.dir_change()
        self.coors_for_dir_change_delete()
        self.movement()

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

    def movement(self):
        """Moves the part based on its direction variable"""
        if self.dir == "RIGHT":
            self.rect.move_ip(self.speed, 0)
        elif self.dir == "LEFT" :
            self.rect.move_ip(-self.speed, 0)
        elif self.dir == "UP":
            self.rect.move_ip(0, -self.speed)
        elif self.dir == "DOWN":
            self.rect.move_ip(0, self.speed)

    def set_spawn_position(self):
        """Sets spawn position based on the movement direction and id number"""
        position = 20
        if self.id_number > 1:
            position = 0

        if self.preview_part.dir == "RIGHT":
            return [self.preview_part.coors[0]-position, self.preview_part.coors[1]]
        elif self.preview_part.dir == "LEFT":
            return [self.preview_part.coors[0]+position, self.preview_part.coors[1]]
        elif self.preview_part.dir == "UP":
            return [self.preview_part.coors[0], self.preview_part.coors[1]+position]
        elif self.preview_part.dir == "DOWN":
            return [self.preview_part.coors[0], self.preview_part.coors[1]-position]
















