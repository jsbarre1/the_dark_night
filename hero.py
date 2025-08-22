import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_SCALE

class Hero(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        # Load and scale the hero image
        original_image = pygame.image.load("Hero.png")
        scaled_size = (int(original_image.get_width() * SPRITE_SCALE), 
                      int(original_image.get_height() * SPRITE_SCALE))
        self.image = pygame.transform.scale(original_image, scaled_size)
        self.rect = self.image.get_rect()
        self.health = 100
        self.age = 0
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        # Get current display surface dimensions for proper boundary checking
        current_surface = pygame.display.get_surface()
        if current_surface:
            current_width = current_surface.get_width()
            current_height = current_surface.get_height()
        else:
            # Fallback to config values if no surface available
            current_width = SCREEN_WIDTH
            current_height = SCREEN_HEIGHT
        
        if self.rect.left > 0:
            if(pressed_keys[pygame.K_LEFT]):
                self.rect.move_ip(-5,0)
        if self.rect.right < current_width:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5,0)
        if self.rect.top > 0:
            if(pressed_keys[pygame.K_UP]):
                self.rect.move_ip(0,-5)
        if (self.rect.bottom) < current_height: 
            if(pressed_keys[pygame.K_DOWN]):
                self.rect.move_ip(0,5)

    def draw(self, surface):
        surface.blit(self.image, self.rect)                
