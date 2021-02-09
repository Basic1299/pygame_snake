import pygame

class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.id_number = 0
        self.size = (20, 20)
        self.color = (0, 100, 0)
        self.coors = [pos_x, pos_y]
        self.coors_for_change_dir = []
        self.tail_length = 0
        
        self.pressed_times = []
        self.current_time = 0

        self.init_dir = ""
        self.dir = ""
        self.speed = 5
        
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.coors)

    def update(self):
        self.movement()
        self.position_update()
##        self.delete_coors_for_dir()

    def time_update(self, current):
        self.current_time = current

    def delete_coors_for_dir(self):
        if len(self.coors_for_change_dir) > 0:
            for time in self.pressed_times:
                if self.current_time - time > (self.tail_length // 5) * 1000:
                    del self.coors_for_change_dir[0]
                
            
    def update_tail(self, tail_len):
        self.tail_length = tail_len

    def position_update(self):
        self.coors = [self.rect.centerx, self.rect.centery]

    def movement(self):
        if self.dir == "RIGHT":
            self.rect.move_ip(self.speed, 0)
        elif self.dir == "LEFT":
            self.rect.move_ip(-self.speed, 0)
        elif self.dir == "UP":
            self.rect.move_ip(0, -self.speed)
        elif self.dir == "DOWN":
            self.rect.move_ip(0, self.speed)
