import pygame
from ui_components.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, DARK_GRAY, GOLD, BATMAN_BLUE, RED, FPS


class GameOverScreen:
    def __init__(self) -> None:
        self.buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50, "RESTART", GOLD, (255, 235, 20)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50, "HOME", BATMAN_BLUE, (45, 45, 132))
        ]
        
    def run(self, display_surface: pygame.Surface, clock: pygame.time.Clock) -> str:
        # Show dramatic red flash first
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                    
                for button in self.buttons:
                    if button.handle_event(event):
                        if button.text == "RESTART":
                            return "restart"
                        elif button.text == "HOME":
                            return "home"
            
            # Draw dark background
            display_surface.fill(DARK_GRAY)
            
            # Draw game over title
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("GAME OVER", True, RED)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            display_surface.blit(title_text, title_rect)
            
            # Draw subtitle
            subtitle_font = pygame.font.Font(None, 36)
            subtitle_text = subtitle_font.render("The Dark Night has fallen...", True, WHITE)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 60))
            display_surface.blit(subtitle_text, subtitle_rect)
            
            # Draw instruction text
            instruction_font = pygame.font.Font(None, 24)
            instruction_text = instruction_font.render("Choose your next move, hero", True, GOLD)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            display_surface.blit(instruction_text, instruction_rect)
            
            # Draw buttons
            for button in self.buttons:
                button.draw(display_surface)
            
            pygame.display.update()
            clock.tick(FPS) 