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
        
        # Use fixed fullscreen dimensions for positioning since game only runs in fullscreen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(40, SCREEN_HEIGHT-40))
        
        self.health: int = health
        self.attack_power: int = attack_power
        self.name: str = name
        
        # Targeting behavior variables
        self.target_speed: float = 1.5  # Slightly faster than wandering, but still slow
        self.target: pygame.sprite.Sprite = hero_target  # Store the hero target directly
    
    def move(self) -> None:
        # Use fixed fullscreen dimensions since game only runs in fullscreen
        current_width: int = SCREEN_WIDTH
        current_height: int = SCREEN_HEIGHT
        
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
        
        # Keep enemy within screen bounds using fixed dimensions
        self.rect.clamp_ip(pygame.Rect(0, 0, current_width, current_height))
 
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect) 
