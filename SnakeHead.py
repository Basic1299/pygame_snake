import pygame


class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, snake_color):
        super().__init__()
        self.name = ""

        self.current_time = pygame.time.get_ticks()
        self.pressed_times = []
        
        self.id_number = 0
        self.size = (20, 20)

        # WORD COLOR
        self.snake_color = snake_color
        # SKIN COLOR
        self.head_color = self.get_head_color()
        self.eyes_color = self.get_eyes_color()

        self.coors = [pos_x, pos_y]
        self.coors_for_change_dir = []
        self.eat_spots = []
        self.spawn_tail = False
        self.tail_length = 0

        self.init_dir = ""
        self.dir = ""
        self.speed = speed

        # Initial visual head state
        self.image = pygame.Surface(self.size)
        self.image.fill(self.head_color)
        pygame.draw.rect(self.image, self.eyes_color, (2, 5, 4, 4), 0)
        pygame.draw.rect(self.image, self.eyes_color, (14, 5, 4, 4), 0)

        self.rect = self.image.get_rect(center=self.coors)

    def update(self):
        self.time_update()
        self.movement()
        self.position_update()
        self.visual_head_update()

        self.head_color = self.get_head_color()
        self.eyes_color = self.get_eyes_color()

    def visual_head_update(self):
        """Changes head state based on moving direction"""
        if self.dir == "LEFT":
            self.image = pygame.Surface(self.size)
            self.image.fill(self.head_color)
            # Eyes
            pygame.draw.rect(self.image, self.eyes_color, (10, 0, 4, 4), 0)
            pygame.draw.rect(self.image, self.eyes_color, (10, 16, 4, 4), 0)
        elif self.dir == "RIGHT":
            self.image = pygame.Surface(self.size)
            self.image.fill(self.head_color)
            # Eyes
            pygame.draw.rect(self.image, self.eyes_color, (6, 0, 4, 4), 0)
            pygame.draw.rect(self.image, self.eyes_color, (6, 16, 4, 4), 0)
        elif self.dir == "UP":
            self.image = pygame.Surface(self.size)
            self.image.fill(self.head_color)
            # Eyes
            pygame.draw.rect(self.image, self.eyes_color, (0, 10, 4, 4), 0)
            pygame.draw.rect(self.image, self.eyes_color, (16, 10, 4, 4), 0)
        elif self.dir == "DOWN":
            self.image = pygame.Surface(self.size)
            self.image.fill(self.head_color)
            # Eyes
            pygame.draw.rect(self.image, self.eyes_color, (0, 6, 4, 4), 0)
            pygame.draw.rect(self.image, self.eyes_color, (16, 6, 4, 4), 0)

    def time_update(self):
        """Measures time in m seconds"""
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

    def get_head_color(self):
        """Based on word color sets color of the head"""
        if self.snake_color == "GREEN":
            return 0, 100, 0
        elif self.snake_color == "RED":
            return 100, 0, 0
        elif self.snake_color == "BLUE":
            return 0, 0, 150

    def get_eyes_color(self):
        """Based on word color sets color of the eyes"""
        if self.snake_color == "GREEN":
            # Red eyes
            return 255, 0, 0
        elif self.snake_color == "RED":
            # Yellow eyes
            return 255, 255, 0
        elif self.snake_color == "BLUE":
            # White eyes
            return 255, 255, 255
        
    def movement(self):
        if self.dir == "RIGHT":
            self.rect.move_ip(self.speed, 0)
        elif self.dir == "LEFT":
            self.rect.move_ip(-self.speed, 0)
        elif self.dir == "UP":
            self.rect.move_ip(0, -self.speed)
        elif self.dir == "DOWN":
            self.rect.move_ip(0, self.speed)
