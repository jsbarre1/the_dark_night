import pygame, sys
from pygame.locals import *
import random, time
from typing import List

from enemy import Enemy
from player import Player
from screens import HomeScreen, OptionsScreen, PauseMenu, GameOverScreen
from config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, DARK_GRAY, GAME_BG, FPS
from weapon import PlayerProjectile


def run_game() -> str:
    player: Player = Player("Absolute")
    firstEnemy: Enemy = Enemy(100, 20, "Sludge Guy", player)

    enemies: pygame.sprite.Group = pygame.sprite.Group()
    enemies.add(firstEnemy)
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(firstEnemy)
    
    # Create pause menu and game over screen
    pause_menu = PauseMenu()
    game_over_screen = GameOverScreen()
    
    player_projectiles: List[PlayerProjectile] = []
    batarang: pygame.Surface = pygame.image.load("sprites/batarang.png")


    while True:
        #Cycles through all events occuring
        mouse_x, mouse_y = pygame.mouse.get_pos()  
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_projectile = PlayerProjectile(player.rect.centerx, player.rect.centery, mouse_x, mouse_y, batarang)
                    player_projectiles.append(new_projectile)
                 
            # Handle pause menu with ESC key
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Show pause menu
                    pause_action = pause_menu.run(DISPLAYSURF, FramePerSec)
                    if pause_action == "quit":
                        pygame.quit()
                        return "quit"
                    elif pause_action == "home":
                        return "home"  # Return to home screen
                    elif pause_action == "resume":
                        continue  # Continue the game
                # Add Tab key to quit the game
                elif event.key == K_TAB:
                    pygame.quit()
                    return "quit"
                # Add Backspace key to quit the game
                elif event.key == K_BACKSPACE:
                    pygame.quit()
                    return "quit"
                # Add Q key to quit the game
                elif event.key == K_q:
                    pygame.quit()
                    return "quit"
     
        DISPLAYSURF.fill(GAME_BG)
     
        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            if isinstance(entity, Player):
                entity.update()
                entity.handle_weapons(DISPLAYSURF)
                # entity.handle_weapons(DISPLAYSURF)  # Commented out until weapon system is fully implemented
            elif isinstance(entity, Enemy):
                entity.move()
        
        for projectile in player_projectiles:
            projectile.fire_player_projectile(DISPLAYSURF)
        
        # Clean up projectiles that go off-screen
        player_projectiles = [p for p in player_projectiles if 
                            0 <= p.x <= SCREEN_WIDTH and 0 <= p.y <= SCREEN_HEIGHT]
     
        #To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollideany(player, enemies):
            # Show game over screen
            game_over_action = game_over_screen.run(DISPLAYSURF, FramePerSec)
            if game_over_action == "quit":
                pygame.quit()
                return "quit"
            elif game_over_action == "home":
                return "home"  # Return to home screen
            elif game_over_action == "restart":
                return "restart"  # Restart the game
             
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
        while True:  # Loop for restart functionality
            game_result = run_game()
            if game_result == "quit":
                pygame.quit()
                sys.exit()
            elif game_result == "home":
                break  # Exit restart loop and go back to home screen
            elif game_result == "restart":
                continue  # Continue the restart loop to start a new game
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
    

