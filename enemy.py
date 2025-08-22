import random
import pygame

from config import SCREEN_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, attack_power, name):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),random.randint(40,SCREEN_WIDTH-40)) 
        self.health = health
        self.attack_power = attack_power
        self.name = name
    
    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
