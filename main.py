import pygame, sys
from pygame.locals import *
import random, time

from enemy import Enemy
from hero import Hero
from config import *


pygame.init()

FramePerSec = pygame.time.Clock()

# Start in windowed mode with reasonable size
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

# Track fullscreen state
is_fullscreen = False

user = Hero("Absolute")
firstEnemy = Enemy(100, 20, "Sludge Guy")

enemies = pygame.sprite.Group()
enemies.add(firstEnemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(user)
all_sprites.add(firstEnemy)

while True:
    
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Handle fullscreen toggle with F11 key
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # ESC key puts game in windowed mode instead of exiting
                if is_fullscreen:
                    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    is_fullscreen = False
            elif event.key == K_F11:
                if is_fullscreen:
                    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    is_fullscreen = False
                else:
                    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    is_fullscreen = True
            # Add F key as alternative fullscreen toggle
            elif event.key == K_f:
                if is_fullscreen:
                    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    is_fullscreen = False
                else:
                    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    is_fullscreen = True
            # Add Q key to quit the game
            elif event.key == K_q:
                pygame.quit()
                sys.exit()
        # Handle window resize events
        elif event.type == VIDEORESIZE:
            if not is_fullscreen:
                # Update the display surface to match the new window size
                new_width = event.w
                new_height = event.h
                DISPLAYSURF = pygame.display.set_mode((new_width, new_height))
                # Update the window caption to show new dimensions
                pygame.display.set_caption(f"Game - {new_width}x{new_height}")

    DISPLAYSURF.fill(WHITE)

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if isinstance(entity, Hero):
            entity.update()
        elif isinstance(entity, Enemy):
            entity.move()

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(user, enemies):
        DISPLAYSURF.fill(RED)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
        
    pygame.display.update()
    FramePerSec.tick(FPS)
    

