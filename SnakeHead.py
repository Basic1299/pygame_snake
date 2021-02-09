import pygame

class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.current_time = pygame.time.get_ticks()
        self.pressed_times = []
        
        self.id_number = 0
        self.size = (20, 20)
        self.color = (0, 100, 0)
        self.coors = [pos_x, pos_y]
        self.coors_for_change_dir = []
        self.eat_spots = []
        self.spawn_tail = False
        self.tail_length = 0

        self.init_dir = ""
        self.dir = ""
        self.speed = 2
        
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.coors)

    def update(self):
        self.time_update()
        self.movement()
        self.position_update()

    def time_update(self):
        self.current_time = pygame.time.get_ticks()
            
    def update_tail(self, tail_len):
        """Calculates and sets the lengths of the tal"""
        self.tail_length = tail_len

    def position_update(self):
        self.coors = [self.rect.centerx, self.rect.centery]

    def create_new_dir_spot(self):
        self.coors_for_change_dir.append((self.coors, self.dir))

    def create_eat_spot(self):
        self.eat_spots.append(self.coors)
        
    def movement(self):
        if self.dir == "RIGHT":
            self.rect.move_ip(self.speed, 0)
        elif self.dir == "LEFT":
            self.rect.move_ip(-self.speed, 0)
        elif self.dir == "UP":
            self.rect.move_ip(0, -self.speed)
        elif self.dir == "DOWN":
            self.rect.move_ip(0, self.speed)
