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
        walking_images: List[pygame.Surface] = None,
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
        
        # Walking animation variables
        self.walking_state: int = 0  # 0 or 1 for two walking states
        self.walking_animation_speed: int = 15  # Frames per walking state change
        self.walking_frame_counter: int = 0
        self.walking_images: List[pygame.Surface] = []  # Two walking state images
        self.is_moving: bool = False
        
        # Setup walking images if provided
        if walking_images and len(walking_images) >= 2:
            self.walking_images = walking_images[:2]
            # Set initial image to first walking state
            self.image = self.walking_images[0].copy()
            self.original_enemy_image = self.walking_images[0].copy()

    @abstractmethod
    def setup_weapon_animations(self) -> None:
        """Setup weapon animations for this specific enemy type"""
        pass
    
    @abstractmethod
    def setup_walking_animations(self) -> None:
        """Setup walking animations for this specific enemy type"""
        pass

    @abstractmethod
    def get_attack_animation_frames(self) -> List[pygame.Surface]:
        """Get the attack animation frames for this enemy type"""
        pass
    
    def get_weapon_animation_frames(self) -> dict:
        """Get all available weapon animation frames from the weapon"""
        if hasattr(self.weapon, 'animation_swing_left') and hasattr(self.weapon, 'animation_swing_right'):
            return {
                "left": self.weapon.animation_swing_left.copy(),
                "right": self.weapon.animation_swing_right.copy()
            }
        return {}
    
    def set_attack_direction(self, direction: str) -> None:
        """Set the attack direction - to be implemented by subclasses"""
        pass
    
    def get_attack_direction(self) -> str:
        """Get the current attack direction"""
        return getattr(self, 'attack_direction', 'right')
    
    def update_walking_animation(self) -> None:
        """Update the walking animation state"""
        if not self.is_moving or not self.walking_images:
            return
            
        self.walking_frame_counter += 1
        
        if self.walking_frame_counter >= self.walking_animation_speed:
            self.walking_frame_counter = 0
            # Toggle between walking states 0 and 1
            self.walking_state = 1 - self.walking_state
            # Update the enemy image to the current walking state
            if self.walking_images and not self.is_attacking:
                self.image = self.walking_images[self.walking_state].copy()
    
    def set_moving_state(self, moving: bool) -> None:
        """Set whether the enemy is currently moving"""
        self.is_moving = moving
        if not moving and self.walking_images:
            # Reset to first walking state when stopped
            self.walking_state = 0
            self.walking_frame_counter = 0
            if not self.is_attacking:
                self.image = self.walking_images[0].copy()
    
    def get_walking_state(self) -> int:
        """Get the current walking state (0 or 1)"""
        return self.walking_state
    
    def set_walking_animation_speed(self, speed: int) -> None:
        """Set the walking animation speed (lower = faster)"""
        self.walking_animation_speed = max(1, speed)  # Ensure speed is at least 1
    
    def reset_walking_animation(self) -> None:
        """Reset walking animation to initial state"""
        self.walking_state = 0
        self.walking_frame_counter = 0
        if self.walking_images and not self.is_attacking:
            self.image = self.walking_images[0].copy()
    
    def set_walking_images(self, walking_images: List[pygame.Surface]) -> None:
        """Set walking images after initialization"""
        if walking_images and len(walking_images) >= 2:
            self.walking_images = walking_images[:2]
            # Update current image if not attacking
            if not self.is_attacking:
                self.image = self.walking_images[self.walking_state].copy()
            # Update original enemy image
            self.original_enemy_image = self.walking_images[0].copy()
        else:
            print("Warning: Invalid walking images provided. Need at least 2 images.")
    
    def get_walking_images(self) -> List[pygame.Surface]:
        """Get the current walking images"""
        return self.walking_images.copy() if self.walking_images else []

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
                # Restore to current walking state or original image
                if self.walking_images and self.is_moving:
                    self.image = self.walking_images[self.walking_state].copy()
                else:
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
            # Determine attack direction if the subclass supports it
            if hasattr(self, 'set_attack_direction') and self.target:
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
            if self.weapon_imgs:
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
            
            # Update walking animation if moving
            if move_x != 0 or move_y != 0:
                self.set_moving_state(True)
                self.update_walking_animation()
            else:
                self.set_moving_state(False)

        else:
            print("No target set for enemy!")
            self.set_moving_state(False)

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
        walking_images: List[pygame.Surface] = None,
    ) -> None:
        # Call parent constructor with sludge-specific name
        super().__init__(health, attack_power, "Sludge", target, weapon, enemy_img)
        
        # Setup weapon animations using the weapon's stored frames
        self.setup_weapon_animations()
        
        # Setup walking animations with provided images
        self.setup_walking_animations(walking_images)
        
        # Set initial weapon image
        if self.weapon_imgs:
            self.current_weapon_img = self.weapon_imgs[0]
            self.original_weapon_img = self.weapon_imgs[0].copy()

    def setup_weapon_animations(self) -> None:
        """Setup weapon animations using the weapon's stored animation frames"""
        if isinstance(self.weapon, EnemySword):
            # Initialize with right swing as default
            self.weapon_imgs = self.weapon.animation_swing_right.copy()
            self.attack_direction = "right"
        else:
            # Fallback for non-sword weapons
            self.weapon_imgs = []
    
    def setup_walking_animations(self, walking_images: List[pygame.Surface] = None) -> None:
        """Setup walking animations using provided images or fallback to default"""
        if walking_images and len(walking_images) >= 2:
            # Use provided walking images
            self.walking_images = walking_images[:2]  # Take first two images
            # Set initial image to first walking state
            self.image = self.walking_images[0].copy()
            self.original_enemy_image = self.walking_images[0].copy()
        else:
            # Fallback to using the current image for both states
            self.walking_images = [self.image, self.image]
            print("Warning: SludgeEnemy using fallback walking images. Provide walking_images parameter for proper animation.")

    def get_attack_animation_frames(self) -> List[pygame.Surface]:
        """Get the attack animation frames for sludge enemy"""
        return self.weapon_imgs.copy()
    
    def get_weapon_animation_frames(self) -> dict:
        """Get all available weapon animation frames from the EnemySword"""
        if isinstance(self.weapon, EnemySword):
            return {
                "left": self.weapon.animation_swing_left.copy(),
                "right": self.weapon.animation_swing_right.copy()
            }
        return {}
    
    def get_sword_animation_info(self) -> dict:
        """Get detailed information about the sword animations"""
        if isinstance(self.weapon, EnemySword):
            return {
                "left_frames": len(self.weapon.animation_swing_left),
                "right_frames": len(self.weapon.animation_swing_right),
                "current_direction": self.attack_direction,
                "current_frame": self.attack_animation_index
            }
        return {}
    
    def get_walking_animation_info(self) -> dict:
        """Get detailed information about the walking animations"""
        return {
            "walking_frames": len(self.walking_images),
            "current_walking_state": self.walking_state,
            "is_moving": self.is_moving,
            "walking_frame_counter": self.walking_frame_counter,
            "walking_animation_speed": self.walking_animation_speed
        }

    def set_attack_direction(self, direction: str) -> None:
        """Set the attack direction and update weapon images accordingly"""
        if isinstance(self.weapon, EnemySword):
            if direction == "left":
                self.weapon_imgs = self.weapon.animation_swing_left.copy()
                self.attack_direction = "left"
            elif direction == "right":
                self.weapon_imgs = self.weapon.animation_swing_right.copy()
                self.attack_direction = "right"
            
            # Reset animation state and update current weapon image
            if self.weapon_imgs:
                self.current_weapon_img = self.weapon_imgs[0]
                # Also update the original weapon image for restoration after attack
                self.original_weapon_img = self.weapon_imgs[0].copy()

    def get_sword_angle(self) -> float:
        """Get the current sword angle based on animation frame"""
        if not self.is_attacking or not self.weapon_imgs:
            return 0.0
        
        # Map animation index to sword angle based on direction
        # These angles correspond to the sludge sword animation frames
        if self.attack_direction == "left":
            # Left swing angles (reverse order for left-facing attack)
            angles = [90, 65, 45, 25, 0, -20, -45, -70, -90]
        else:
            # Right swing angles (standard order for right-facing attack)
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

            # Start with first weapon frame from the selected direction
            if self.weapon_imgs:
                self.current_weapon_img = self.weapon_imgs[0]
