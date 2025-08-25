import pygame, sys
from pygame.locals import *
import random, time
from typing import List

from enemy import Enemy, SludgeEnemy
from player import Player
from screens import HomeScreen, OptionsScreen, PauseMenu, GameOverScreen
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    RED,
    DARK_GRAY,
    GAME_BG,
    FPS,
    WHITE,
    BATMAN_BLUE,
)
from weapon import EnemySword, PlayerProjectile, WeaponType


def display_health(display: pygame.Surface, player: Player) -> None:
    """Display the player's health as a red status bar on the top right of the screen"""
    # Health bar dimensions and position
    bar_width = 200
    bar_height = 25
    bar_x = SCREEN_WIDTH - bar_width - 20
    bar_y = 20

    # Draw background rectangle (empty health bar)
    background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    pygame.draw.rect(display, DARK_GRAY, background_rect)
    pygame.draw.rect(display, WHITE, background_rect, 2)  # White border

    # Calculate current health percentage and fill the bar
    health_percentage = player.health / 100.0
    current_health_width = int(bar_width * health_percentage)

    # Draw the red health bar
    if current_health_width > 0:
        health_rect = pygame.Rect(bar_x, bar_y, current_health_width, bar_height)
        pygame.draw.rect(display, RED, health_rect)

    # Add "HEALTH" label above the bar
    font = pygame.font.Font(None, 24)
    label_text = "HEALTH"
    label_surface = font.render(label_text, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.centerx = bar_x + bar_width // 2
    label_rect.bottom = bar_y - 5

    display.blit(label_surface, label_rect)


def run_game() -> str:
    player: Player = Player("Absolute")
    main_display_scroll = [0, 0]
    sludge_sword_img: pygame.Surface = pygame.image.load(
        "sprites/sludge/sludge_sword_0.png"
    )
    sludge_img: pygame.Surface = pygame.image.load("sprites/sludge/sludge_neutral.png")
    # Load all sword animation frames
    sludge_sword_imgs_swing_left: List[pygame.Surface] = [
        pygame.image.load("sprites/sludge/sludge_sword_20.png").convert_alpha(),
        pygame.image.load("sprites/sludge/sludge_sword_45.png").convert_alpha(),
        pygame.image.load("sprites/sludge/sludge_sword_70.png").convert_alpha(),
        pygame.image.load("sprites/sludge/sludge_sword_90.png").convert_alpha(),
    ]

    sludge_sword_imgs_swing_right: List[pygame.Surface] = [
        pygame.image.load("sprites/sludge/sludge_sword_-25.png").convert_alpha(),
        pygame.image.load("sprites/sludge/sludge_sword_-45.png").convert_alpha(),
        pygame.image.load("sprites/sludge/sludge_sword_-65.png").convert_alpha(),
        pygame.image.load("sprites/sludge/sludge_sword_-90.png").convert_alpha(),
    ]

    sludge_sword: EnemySword = EnemySword(
        "sludge_sword",
        WeaponType.SWORD,
        3,
        sludge_sword_img,
        sludge_sword_imgs_swing_left,
        sludge_sword_imgs_swing_right,
    )

    firstEnemySludge: SludgeEnemy = SludgeEnemy(
        100, 3, player, sludge_sword, sludge_img
    )

    enemies: pygame.sprite.Group = pygame.sprite.Group()
    enemies.add(firstEnemySludge)
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(firstEnemySludge)

    # Create pause menu and game over screen
    pause_menu = PauseMenu()
    game_over_screen = GameOverScreen()

    player_projectiles: List[PlayerProjectile] = []
    batarang: pygame.Surface = pygame.image.load("sprites/batarang.png")

    # Invincibility frame system
    invincibility_duration = 200  # 1 second in milliseconds
    last_damage_time = 0
    damaged_enemies = set()  # Track which enemies have recently damaged the player

    while True:
        # Cycles through all events occuring
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_projectile = PlayerProjectile(
                        player.rect.centerx,
                        player.rect.centery,
                        mouse_x,
                        mouse_y,
                        batarang,
                    )
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

            # Handle invincibility timer events
            elif (
                event.type >= pygame.USEREVENT and event.type < pygame.USEREVENT + 1000
            ):
                # Remove enemies from damaged set after invincibility period
                for enemy in list(damaged_enemies):
                    if event.type == pygame.USEREVENT + hash(enemy) % 1000:
                        damaged_enemies.discard(enemy)

        DISPLAYSURF.fill(GAME_BG)

        # Moves and Re-draws all Sprites
        for entity in all_sprites:
            if isinstance(entity, Player):
                entity.update()
                entity.handle_weapons(DISPLAYSURF)
                # entity.handle_weapons(DISPLAYSURF)  # Commented out until weapon system is fully implemented
                DISPLAYSURF.blit(entity.image, entity.rect)
            elif isinstance(entity, Enemy):
                entity.move()
                entity.draw(DISPLAYSURF)
            else:
                DISPLAYSURF.blit(entity.image, entity.rect)

        for projectile in player_projectiles:
            projectile.fire_player_projectile(DISPLAYSURF)

        # Clean up projectiles that go off-screen
        player_projectiles = [
            p
            for p in player_projectiles
            if 0 <= p.x <= SCREEN_WIDTH and 0 <= p.y <= SCREEN_HEIGHT
        ]

        # Display player health on top right
        display_health(DISPLAYSURF, player)

        if pygame.sprite.spritecollideany(player, enemies):
            current_time = pygame.time.get_ticks()

            # Get the enemy that collided with the player
            for enemy in enemies:
                if pygame.sprite.collide_rect(player, enemy):
                    # Check if enough time has passed since last damage and enemy hasn't recently damaged player
                    if (
                        current_time - last_damage_time >= invincibility_duration
                        and enemy not in damaged_enemies
                    ):
                        # Reduce player health by enemy's attack power
                        player.health -= enemy.attack_power
                        # Ensure health doesn't go below 0
                        if player.health < 0:
                            player.health = 0

                        # Update invincibility tracking
                        last_damage_time = current_time
                        damaged_enemies.add(enemy)

                        # Remove enemy from damaged set after invincibility period
                        pygame.time.set_timer(
                            pygame.USEREVENT + hash(enemy) % 1000,
                            invincibility_duration,
                        )

                    break  # Only process one enemy per collision check

        # Check if player is dead
        if player.health <= 0:
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
DISPLAYSURF: pygame.Surface = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
)
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
