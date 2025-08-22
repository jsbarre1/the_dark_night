import random
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SCALE


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, attack_power, name):
        super().__init__()
        # Load and scale the enemy image
        original_image = pygame.image.load("Enemy.png")
        scaled_size = (int(original_image.get_width() * SPRITE_SCALE), 
                      int(original_image.get_height() * SPRITE_SCALE))
        self.image = pygame.transform.scale(original_image, scaled_size)
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),random.randint(40,SCREEN_HEIGHT-40)) 
        self.health = health
        self.attack_power = attack_power
        self.name = name
        
        # Wandering behavior variables
        self.wander_speed = 1  # Slow movement speed
        self.direction_x = random.choice([-1, 1])  # Random horizontal direction
        self.direction_y = random.choice([-1, 1])  # Random vertical direction
        self.change_direction_timer = 0
        self.change_direction_interval = random.randint(60, 180)  # Change direction every 1-3 seconds (60 FPS)
    
    def move(self):
        # Get current display surface dimensions for proper boundary checking
        current_surface = pygame.display.get_surface()
        if current_surface:
            current_width = current_surface.get_width()
            current_height = current_surface.get_height()
        else:
            # Fallback to config values if no surface available
            current_width = SCREEN_WIDTH
            current_height = SCREEN_HEIGHT
            
        # Move the enemy slowly in current direction
        self.rect.move_ip(self.direction_x * self.wander_speed, self.direction_y * self.wander_speed)
        
        # Bounce off screen edges using current dimensions
        if self.rect.left <= 0 or self.rect.right >= current_width:
            self.direction_x *= -1  # Reverse horizontal direction
        if self.rect.top <= 0 or self.rect.bottom >= current_height:
            self.direction_y *= -1  # Reverse vertical direction
            
        # Keep enemy within screen bounds
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        
        # Randomly change direction occasionally
        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_direction_interval:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.change_direction_timer = 0
            self.change_direction_interval = random.randint(60, 180)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
