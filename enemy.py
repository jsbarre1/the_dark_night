import math
import random
import pygame
from typing import Tuple, List

from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health: int, attack_power: int, name: str, target: pygame.sprite.Sprite, weapon_img: pygame.Surface, enemy_img: pygame.Surface) -> None:
        super().__init__()
        self.image: pygame.Surface = enemy_img
        self.rect: pygame.Rect = self.image.get_rect()
        
        # Use fixed fullscreen dimensions for positioning since game only runs in fullscreen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(40, SCREEN_HEIGHT-40))
        
        self.health: int = health
        self.attack_power: int = attack_power
        self.name: str = name
        self.reset_offset = 0
        self.offset_x = random.randrange(-300,300)
        self.offset_y = random.randrange(-300, 300)
        
        # Targeting behavior variables
        self.target_speed: float = 2.0  # Movement speed
        self.target: pygame.sprite.Sprite = target  # Store the hero target directly
        
        # Store weapon image for rendering
        self.weapon_img: pygame.Surface = weapon_img
        
        # Sword swinging animation variables
        self.attack_range: int = 500
        self.is_attacking: bool = False
        self.attack_animation_speed: int = 8  # Frames per animation update
        self.attack_frame_counter: int = 0
        self.attack_animation_index: int = 0
        
        # Load sword swinging animation frames
        self.sword_animation_frames: List[pygame.Surface] = []
        self.load_sword_animation_frames()
        
        # Store original image for when not attacking
        self.original_image: pygame.Surface = self.image.copy()
        
        # Store original position for consistent animation positioning
        self.original_position: Tuple[int, int] = (self.rect.centerx, self.rect.centery)
    
    def load_sword_animation_frames(self) -> None:
        """Load the sword swinging animation frames for sludge"""
        try:
            # Load the sword swinging animation frames
            frame_files = [
                "sprites/sludge/sludge_left_20.png",
                "sprites/sludge/sludge_left_45.png", 
                "sprites/sludge/sludge_left_65.png",
                "sprites/sludge/sludge_left_90.png"
            ]
            
            # Find the maximum dimensions to create consistent frame sizes
            max_width = 0
            max_height = 0
            original_frames = []
            
            for frame_file in frame_files:
                frame_img = pygame.image.load(frame_file).convert_alpha()
                original_frames.append(frame_img)
                max_width = max(max_width, frame_img.get_width())
                max_height = max(max_height, frame_img.get_height())
            
            # Create consistent-sized frames with proper positioning
            for i, original_frame in enumerate(original_frames):
                # Create a surface with the maximum dimensions
                consistent_frame = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
                
                # Calculate offset to keep sludge character in the same position
                # Since sludge is on the right side, we'll align the right edges
                offset_x = max_width - original_frame.get_width()
                offset_y = max_height - original_frame.get_height()
                
                # Blit the original frame onto the consistent surface
                consistent_frame.blit(original_frame, (offset_x, offset_y))
                
                self.sword_animation_frames.append(consistent_frame)
                
        except Exception as e:
            print(f"Error loading sword animation frames: {e}")
            # If loading fails, create a simple colored rectangle as fallback
            fallback_surface = pygame.Surface((32, 32))
            fallback_surface.fill((255, 0, 0))  # Red fallback
            self.sword_animation_frames = [fallback_surface] * 4
    
    def is_within_attack_range(self) -> bool:
        """Check if the enemy is within attack range of the target"""
        if not self.target:
            return False
        
        distance = math.sqrt(
            (self.rect.centerx - self.target.rect.centerx) ** 2 +
            (self.rect.centery - self.target.rect.centery) ** 2
        )
        return distance <= self.attack_range
    
    def update_attack_animation(self) -> None:
        """Update the sword swinging animation"""
        if not self.is_attacking:
            return
            
        self.attack_frame_counter += 1
        
        if self.attack_frame_counter >= self.attack_animation_speed:
            self.attack_frame_counter = 0
            self.attack_animation_index += 1
            
            # Loop through animation frames
            if self.attack_animation_index >= len(self.sword_animation_frames):
                self.attack_animation_index = 0
                # End attack after one complete cycle
                self.is_attacking = False
                self.image = self.original_image.copy()
                # Restore original rect and position
                self.rect = self.image.get_rect()
                self.rect.center = self.original_position
            else:
                # Update to next animation frame
                self.image = self.sword_animation_frames[self.attack_animation_index]
                # Maintain the same center position
                self.rect = self.image.get_rect()
                self.rect.center = self.original_position
    
    def start_attack_animation(self) -> None:
        """Start the sword swinging attack animation"""
        if not self.is_attacking and self.sword_animation_frames:
            self.is_attacking = True
            self.attack_animation_index = 0
            self.attack_frame_counter = 0
            
            # Store the current position before starting animation
            self.original_position = (self.rect.centerx, self.rect.centery)
            
            # Start with first frame
            self.image = self.sword_animation_frames[0]
            
            # Ensure the rect maintains the same center position
            self.rect = self.image.get_rect()
            self.rect.center = self.original_position
    
    def is_attacking_now(self) -> bool:
        """Check if the enemy is currently performing an attack animation"""
        return self.is_attacking
    
    def move(self) -> None:
        # Use fixed fullscreen dimensions since game only runs in fullscreen
        current_width: int = SCREEN_WIDTH
        current_height: int = SCREEN_HEIGHT
        
        if self.target:
            # Calculate distance to hero
            target_x, target_y = self.target.rect.centerx, self.target.rect.centery
            
            # Check if within attack range and start attack animation
            if self.is_within_attack_range() and not self.is_attacking:
                self.start_attack_animation()
            
            # Update attack animation if currently attacking
            self.update_attack_animation()
                
            if self.reset_offset == 0:
                self.offset_x = random.randrange(-300,300)
                self.offset_y = random.randrange(-300, 300)
                self.reset_offset = random.randrange(120,150)
            else:
                self.reset_offset -= 1  
            
            # Calculate target position with offset
            target_with_offset_x = target_x + self.offset_x
            target_with_offset_y = target_y + self.offset_y
            
            # Calculate direction to move
            move_x = 0
            move_y = 0
            
            if target_with_offset_x > self.rect.centerx:
                move_x = self.target_speed
            elif target_with_offset_x < self.rect.centerx:
                move_x = -self.target_speed
                
            if target_with_offset_y > self.rect.centery:
                move_y = self.target_speed
            elif target_with_offset_y < self.rect.centery:
                move_y = -self.target_speed
            
            # Apply movement
            self.rect.move_ip(move_x, move_y)
                    
        else:
            print("No target set for enemy!")
        
        # Keep enemy within screen bounds using fixed dimensions
        self.rect.clamp_ip(pygame.Rect(0, 0, current_width, current_height))
 
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect) 
        
