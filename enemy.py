import math
import random
import pygame
from typing import List, Optional
from abc import ABC, abstractmethod

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from weapon import Weapon, EnemySword

class Enemy(pygame.sprite.Sprite, ABC):
    """Abstract base class for all enemies"""
    
    def __init__(
        self,
        health: int,
        attack_power: int,
        name: str,
        target: pygame.sprite.Sprite,
        weapon: Weapon,
        enemy_img: pygame.Surface,
    ) -> None:
        super().__init__()
        self.image: pygame.Surface = enemy_img
        self.rect: pygame.Rect = self.image.get_rect()

        # Use fixed fullscreen dimensions for positioning since game only runs in fullscreen
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(40, SCREEN_HEIGHT - 40),
        )

        self.health: int = health
        self.attack_power: int = attack_power
        self.name: str = name
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)

        # Targeting behavior variables
        self.target_speed: float = 2.0  # Movement speed
        self.target: pygame.sprite.Sprite = target  # Store the hero target directly

        # Weapon and animation variables - to be implemented by subclasses
        self.weapon: Weapon = weapon
        self.weapon_imgs: List[pygame.Surface] = []
        self.current_weapon_img: Optional[pygame.Surface] = None

        # Attack animation variables
        self.attack_range: int = 500
        self.is_attacking: bool = False
        self.attack_animation_speed: int = 8  # Frames per animation update
        self.attack_frame_counter: int = 0
        self.attack_animation_index: int = 0
        self.attack_direction: str = "right"  # Default attack direction

        # Store original images for when not attacking
        self.original_enemy_image: pygame.Surface = self.image.copy()
        self.original_weapon_img: Optional[pygame.Surface] = None

    @abstractmethod
    def setup_weapon_animations(self) -> None:
        """Setup weapon animations for this specific enemy type"""
        pass

    @abstractmethod
    def get_attack_animation_frames(self) -> List[pygame.Surface]:
        """Get the attack animation frames for this enemy type"""
        pass

    def is_within_attack_range(self) -> bool:
        """Check if the enemy is within attack range of the target"""
        if not self.target:
            return False

        distance = math.sqrt(
            (self.rect.centerx - self.target.rect.centerx) ** 2
            + (self.rect.centery - self.target.rect.centery) ** 2
        )
        return distance <= self.attack_range

    def update_attack_animation(self) -> None:
        """Update the attack animation"""
        if not self.is_attacking:
            return

        self.attack_frame_counter += 1

        if self.attack_frame_counter >= self.attack_animation_speed:
            self.attack_frame_counter = 0
            self.attack_animation_index += 1

            # Loop through animation frames
            if self.attack_animation_index >= len(self.weapon_imgs):
                self.attack_animation_index = 0
                # End attack after one complete cycle
                self.is_attacking = False
                # Restore original images
                self.image = self.original_enemy_image.copy()
                self.current_weapon_img = (
                    self.original_weapon_img.copy()
                    if self.original_weapon_img
                    else None
                )
            else:
                # Update to next weapon frame
                self.current_weapon_img = self.weapon_imgs[self.attack_animation_index]

    def start_attack_animation(self) -> None:
        """Start the attack animation"""
        if not self.is_attacking and self.weapon_imgs:
            self.is_attacking = True
            self.attack_animation_index = 0
            self.attack_frame_counter = 0

            # Start with first weapon frame
            self.current_weapon_img = self.weapon_imgs[0]

    def is_attacking_now(self) -> bool:
        """Check if the enemy is currently performing an attack animation"""
        return self.is_attacking

    def move(self) -> None:
        """Move the enemy towards the target with offset behavior"""
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
                self.offset_x = random.randrange(-300, 300)
                self.offset_y = random.randrange(-300, 300)
                self.reset_offset = random.randrange(120, 150)
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
        """Draw the enemy and its weapon"""
        # Draw the enemy
        surface.blit(self.image, self.rect)

        # Draw the weapon if it exists
        if self.current_weapon_img:
            # Position the weapon relative to the enemy
            weapon_rect = self.current_weapon_img.get_rect()
            weapon_rect.center = self.rect.center
            surface.blit(self.current_weapon_img, weapon_rect)


class SludgeEnemy(Enemy):
    """Sludge enemy with sword-wielding capabilities"""
    
    def __init__(
        self,
        health: int,
        attack_power: int,
        target: pygame.sprite.Sprite,
        weapon: EnemySword,
        enemy_img: pygame.Surface,
    ) -> None:
        # Call parent constructor with sludge-specific name
        super().__init__(health, attack_power, "Sludge", target, weapon, enemy_img)
        
        # Setup weapon animations using the weapon's stored frames
        self.setup_weapon_animations()
        
        # Set initial weapon image
        if self.weapon_imgs:
            self.current_weapon_img = self.weapon_imgs[0]
            self.original_weapon_img = self.weapon_imgs[0].copy()

    def setup_weapon_animations(self) -> None:
        """Setup weapon animations using the weapon's stored animation frames"""
        if isinstance(self.weapon, EnemySword):
            # Use the weapon's stored animation frames
            # Default to right swing, can be changed based on attack direction
            self.weapon_imgs = self.weapon.animation_swing_right.copy()
            self.attack_direction = "right"
        else:
            # Fallback for non-sword weapons
            self.weapon_imgs = []

    def get_attack_animation_frames(self) -> List[pygame.Surface]:
        """Get the attack animation frames for sludge enemy"""
        return self.weapon_imgs.copy()

    def set_attack_direction(self, direction: str) -> None:
        """Set the attack direction and update weapon images accordingly"""
        if isinstance(self.weapon, EnemySword):
            if direction == "left":
                self.weapon_imgs = self.weapon.animation_swing_left.copy()
                self.attack_direction = "left"
            elif direction == "right":
                self.weapon_imgs = self.weapon.animation_swing_right.copy()
                self.attack_direction = "right"
            
            # Reset animation state
            if self.weapon_imgs:
                self.current_weapon_img = self.weapon_imgs[0]

    def get_sword_angle(self) -> float:
        """Get the current sword angle based on animation frame"""
        if not self.is_attacking or not self.weapon_imgs:
            return 0.0
        
        # Map animation index to sword angle based on direction
        if self.attack_direction == "left":
            # Left swing angles (reverse order)
            angles = [90, 65, 45, 25, 0, -20, -45, -70, -90]
        else:
            # Right swing angles
            angles = [-90, -65, -45, -25, 0, 20, 45, 70, 90]
        
        if self.attack_animation_index < len(angles):
            return angles[self.attack_animation_index]
        return 0.0

    def start_attack_animation(self) -> None:
        """Start the attack animation with direction awareness"""
        if not self.is_attacking and self.weapon_imgs:
            # Determine attack direction based on target position
            if self.target:
                target_x = self.target.rect.centerx
                enemy_x = self.rect.centerx
                
                # Set attack direction based on target position relative to enemy
                if target_x < enemy_x:
                    self.set_attack_direction("left")
                else:
                    self.set_attack_direction("right")
            
            self.is_attacking = True
            self.attack_animation_index = 0
            self.attack_frame_counter = 0

            # Start with first weapon frame
            self.current_weapon_img = self.weapon_imgs[0]
