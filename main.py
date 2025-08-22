import pygame, sys
from pygame.locals import *
import random, time
from typing import List

from enemy import Enemy
from hero import Hero
from screens import HomeScreen, OptionsScreen
from config import *


def run_game() -> None:
    user: Hero = Hero("Absolute")
    firstEnemy: Enemy = Enemy(100, 20, "Sludge Guy", user)

    enemies: pygame.sprite.Group = pygame.sprite.Group()
    enemies.add(firstEnemy)
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()
    all_sprites.add(user)
    all_sprites.add(firstEnemy)

    while True:
        #Cycles through all events occuring  
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Handle exit keys
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # ESC key quits the game
                    pygame.quit()
                    sys.exit()
                # Add Tab key to quit the game
                elif event.key == K_TAB:
                    pygame.quit()
                    sys.exit()
                # Add Backspace key to quit the game
                elif event.key == K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                # Add Q key to quit the game
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()
     
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


# Main game loop
pygame.init()

FramePerSec: pygame.time.Clock = pygame.time.Clock()

# Start in fullscreen mode only
DISPLAYSURF: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("The Dark Night - Home Screen")

# Create screens
home_screen = HomeScreen()
options_screen = OptionsScreen()

# Main menu loop
while True:
    # Show home screen
    action = home_screen.run(DISPLAYSURF, FramePerSec)
    
    if action == "play":
        # Start the game
        run_game()
    elif action == "options":
        # Show options screen
        options_action = options_screen.run(DISPLAYSURF, FramePerSec)
        if options_action == "quit":
            pygame.quit()
            sys.exit()
        elif options_action == "back":
            continue  # Go back to home screen
    elif action == "quit":
        # Quit the game
        pygame.quit()
        sys.exit()
    

