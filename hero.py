import pygame
from typing import Tuple

from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_SCALE


class Hero(pygame.sprite.Sprite):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        
        # Load and scale the hero images
        self.original_image: pygame.Surface = pygame.image.load("sprites/batman_idle.png")
        self.batman_down1: pygame.Surface = pygame.image.load("sprites/batman_walking_down1.png")
        self.batman_down2: pygame.Surface = pygame.image.load("sprites/batman_walking_down2.png")
        self.batman_up1: pygame.Surface = pygame.image.load("sprites/batman_walking_up1.png")
        self.batman_up2: pygame.Surface = pygame.image.load("sprites/batman_walking_up2.png")
        
        # Scale all images
        scaled_size: Tuple[int, int] = (int(self.original_image.get_width() * SPRITE_SCALE), 
                                      int(self.original_image.get_height() * SPRITE_SCALE))
        
        self.image: pygame.Surface = pygame.transform.scale(self.original_image, scaled_size)
        self.batman_down1_scaled: pygame.Surface = pygame.transform.scale(self.batman_down1, scaled_size)
        self.batman_down2_scaled: pygame.Surface = pygame.transform.scale(self.batman_down2, scaled_size)
        self.batman_up1_scaled: pygame.Surface = pygame.transform.scale(self.batman_up1, scaled_size)
        self.batman_up2_scaled: pygame.Surface = pygame.transform.scale(self.batman_up2, scaled_size)
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.health: int = 100
        self.age: int = 0
        
        # Animation variables
        self.animation_frame: int = 0
        self.animation_speed: int = 0
        self.is_walking_down: bool = False
        self.is_walking_up: bool = False
    
    def update(self) -> None:
        pressed_keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        
        # Use fixed fullscreen dimensions since game only runs in fullscreen
        current_width: int = SCREEN_WIDTH
        current_height: int = SCREEN_HEIGHT
        
        # Reset walking flags
        self.is_walking_down = False
        self.is_walking_up = False
        
        if self.rect.left > 0:
            if(pressed_keys[pygame.K_LEFT]):
                self.rect.move_ip(-5,0)
        if self.rect.right < current_width:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5,0)
        if self.rect.top > 0:
            if(pressed_keys[pygame.K_UP]):
                self.rect.move_ip(0,-5)
                self.is_walking_up = True
        if (self.rect.bottom) < current_height: 
            if pressed_keys[pygame.K_DOWN]:
                self.rect.move_ip(0,5)
                self.is_walking_down = True
        
        # Update animation
        self._update_animation()
    
    def _update_animation(self) -> None:
        """Update the walking animation when moving up or down"""
        if self.is_walking_down:
            self.animation_speed += 1
            # Change frame every 8 updates (adjust this value to control animation speed)
            if self.animation_speed >= 8:
                self.animation_frame = (self.animation_frame + 1) % 2
                self.animation_speed = 0
                
                # Update the image based on current frame
                if self.animation_frame == 0:
                    self.image = self.batman_down1_scaled
                else:
                    self.image = self.batman_down2_scaled
        elif self.is_walking_up:
            # Use the walking up sprite animation
            self.animation_speed += 1
            # Change frame every 8 updates (adjust this value to control animation speed)
            if self.animation_speed >= 8:
                self.animation_frame = (self.animation_frame + 1) % 2
                self.animation_speed = 0
                
                # Update the image based on current frame
                if self.animation_frame == 0:
                    self.image = self.batman_up1_scaled
                else:
                    self.image = self.batman_up2_scaled
        else:
            # Reset to default image when not walking
            self.image = pygame.transform.scale(self.original_image, 
                                             (int(self.original_image.get_width() * SPRITE_SCALE), 
                                              int(self.original_image.get_height() * SPRITE_SCALE)))
            self.animation_frame = 0
            self.animation_speed = 0

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)                
