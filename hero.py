import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH

class Hero(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = pygame.image.load("Hero.png")
        self.rect = self.image.get_rect()
        self.health = 100
        self.age = 0
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if(pressed_keys[pygame.K_LEFT]):
                self.rect.move_ip(-5,0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5,0)
        if self.rect.top > 0:
            if(pressed_keys[pygame.K_UP]):
                self.rect.move_ip(0,-5)
        if (self.rect.bottom) < SCREEN_HEIGHT: 
            if(pressed_keys[pygame.K_DOWN]):
                self.rect.move_ip(0,5)

    def draw(self, surface):
        surface.blit(self.image, self.rect)                
