import pygame
from ui_components.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, BLUE, RED, WHITE, BLACK, DARK_GRAY, GOLD, BATMAN_BLUE, FPS


class HomeScreen:
    def __init__(self) -> None:
        self.buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50, "PLAY", GOLD, (255, 235, 20)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50, "OPTIONS", BATMAN_BLUE, (45, 45, 132)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50, "QUIT", RED, (159, 20, 20))
        ]
        
    def run(self, display_surface: pygame.Surface, clock: pygame.time.Clock) -> str:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                    
                for button in self.buttons:
                    if button.handle_event(event):
                        if button.text == "PLAY":
                            return "play"
                        elif button.text == "OPTIONS":
                            return "options"
                        elif button.text == "QUIT":
                            return "quit"
            
            # Draw Batman-themed background
            display_surface.fill(DARK_GRAY)
            
            # Draw title with Batman theme
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("THE DARK NIGHT", True, GOLD)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            display_surface.blit(title_text, title_rect)
            
            # Draw subtitle
            subtitle_font = pygame.font.Font(None, 36)
            subtitle_text = subtitle_font.render("An Adventure", True, WHITE)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 60))
            display_surface.blit(subtitle_text, subtitle_rect)
            
            # Draw buttons
            for button in self.buttons:
                button.draw(display_surface)
            
            pygame.display.update()
            clock.tick(FPS) 