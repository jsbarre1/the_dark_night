import pygame
from ui_components.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, DARK_GRAY, GOLD, BATMAN_BLUE, FPS


class PauseMenu:
    def __init__(self) -> None:
        self.buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30, 200, 50, "RESUME", GOLD, (255, 235, 20)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50, "HOME", BATMAN_BLUE, (45, 45, 132))
        ]
        
    def run(self, display_surface: pygame.Surface, clock: pygame.time.Clock) -> str:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "resume"  # ESC to resume game
                    
                for button in self.buttons:
                    if button.handle_event(event):
                        if button.text == "RESUME":
                            return "resume"
                        elif button.text == "HOME":
                            return "home"
            
            # Draw semi-transparent overlay (pause effect)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)  # Semi-transparent
            overlay.fill(DARK_GRAY)
            display_surface.blit(overlay, (0, 0))
            
            # Draw pause menu background
            menu_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100, 300, 200)
            pygame.draw.rect(display_surface, DARK_GRAY, menu_rect)
            pygame.draw.rect(display_surface, GOLD, menu_rect, 3)  # Gold border
            
            # Draw title
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("GAME PAUSED", True, GOLD)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
            display_surface.blit(title_text, title_rect)
            
            # Draw instructions
            instruction_font = pygame.font.Font(None, 24)
            instruction_text = instruction_font.render("Press ESC or click RESUME to continue", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))
            display_surface.blit(instruction_text, instruction_rect)
            
            # Draw buttons
            for button in self.buttons:
                button.draw(display_surface)
            
            pygame.display.update()
            clock.tick(FPS) 