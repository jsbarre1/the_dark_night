import random
import pygame
from typing import Tuple

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SCALE


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health: int, attack_power: int, name: str, hero_target: pygame.sprite.Sprite) -> None:
        super().__init__()
        # Load and scale the enemy image
        original_image: pygame.Surface = pygame.image.load("sprites/Enemy.png")
        scaled_size: Tuple[int, int] = (int(original_image.get_width() * SPRITE_SCALE), 
                                      int(original_image.get_height() * SPRITE_SCALE))
        self.image: pygame.Surface = pygame.transform.scale(original_image, scaled_size)
        self.rect: pygame.Rect = self.image.get_rect()
        
        # Get current display surface dimensions for proper positioning
        current_surface: pygame.Surface | None = pygame.display.get_surface()
        if current_surface:
            current_width = current_surface.get_width()
            current_height = current_surface.get_height()
        else:
            # Fallback to config values if no surface available
            current_width = SCREEN_WIDTH
            current_height = SCREEN_HEIGHT
            
        self.rect.center = (random.randint(40, current_width-40), random.randint(40, current_height-40))
        
        self.health: int = health
        self.attack_power: int = attack_power
        self.name: str = name
        
        # Targeting behavior variables
        self.target_speed: float = 1.5  # Slightly faster than wandering, but still slow
        self.target: pygame.sprite.Sprite = hero_target  # Store the hero target directly
    
    def move(self) -> None:
        # Get current display surface dimensions for proper boundary checking
        current_surface: pygame.Surface | None = pygame.display.get_surface()
        current_width: int
        current_height: int
        if current_surface:
            current_width = current_surface.get_width()
            current_height = current_surface.get_height()
        else:
            # Fallback to config values if no surface available
            current_width = SCREEN_WIDTH
            current_height = SCREEN_HEIGHT
        
        if self.target:
            # Calculate distance to hero
            dx: float = self.target.rect.centerx - self.rect.centerx
            dy: float = self.target.rect.centery - self.rect.centery
            distance: float = (dx**2 + dy**2)**0.5  # Pythagorean theorem
            
            
            # Always move towards hero regardless of distance
            if distance > 0:  # Avoid division by zero
                dx_normalized: float = dx / distance
                dy_normalized: float = dy / distance
                
                # Move towards hero
                self.rect.move_ip(dx_normalized * self.target_speed, dy_normalized * self.target_speed)
        else:
            print("No target set for enemy!")
        
        # Keep enemy within screen bounds using current dimensions
        self.rect.clamp_ip(pygame.Rect(0, 0, current_width, current_height))
 
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect) 
