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
    
    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
