from ast import List
import math

import pygame
from enum import Enum


class WeaponType(Enum):
    SWORD = "sword"
    SPECIAL = "special"
    BOW = "bow"
    GUN = "gun"


class Weapon:
    def __init__(self, name: str, type: WeaponType, damage: int, img: pygame.Surface):
        self.name = name
        self.damage = damage
        self.img = img
        self.type = type


class PlayerWeapon(Weapon):
    def __init__(self, name: str, type: WeaponType, damage: int, img: pygame.Surface):
        super().__init__(name, damage, img)


class EnemyWeapon(Weapon):
    def __init__(self, name: str, type: WeaponType, damage: int, img: pygame.Surface):
        super().__init__(name, damage, img)


class EnemySword(EnemyWeapon):
    def __init__(
        self,
        name: str,
        type: WeaponType,
        damage: int,
        img: pygame.Surface,
        animation_swing_left: List[pygame.Surface],
        animation_swing_right: List[pygame.Surface],
    ):
        super().__init__(name, damage, img)
        self.animation_swing_left = animation_swing_left
        self.animation_swing_right = animation_swing_right


class PlayerProjectile:
    def __init__(self, x, y, mouse_x, mouse_y, projectile_image: pygame.Surface):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.projectile_image = projectile_image
        self.speed = 15
        # Calculate angle from player position to mouse position
        self.angle = math.atan2(mouse_y - y, mouse_x - x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

        # Create a rect for better positioning
        self.rect = self.projectile_image.get_rect()
        self.rect.center = (x, y)

        # Add rotation counter for spinning effect
        self.rotation_counter = 0

    def fire_player_projectile(self, display):
        self.x += int(self.x_vel)
        self.y += int(self.y_vel)

        # Update the rect position
        self.rect.center = (self.x, self.y)

        # Calculate rotation angle and draw rotated projectile
        rotation_angle = math.degrees(math.atan2(self.y_vel, self.x_vel))
        # Add 90 degrees to make the batarang point in the right direction
        rotation_angle += 90

        self.rotation_counter += 30
        rotation_angle += self.rotation_counter

        rotated_image = pygame.transform.rotate(self.projectile_image, rotation_angle)

        # Get the rect for the rotated image and center it
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (self.x + 30, self.y + 40)

        # Draw the rotated projectile
        display.blit(rotated_image, rotated_rect)
