import pygame
from ui_components.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, BLUE, RED, WHITE, BLACK, FPS


class HomeScreen:
    def __init__(self) -> None:
        self.buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50, "PLAY", GREEN, (0, 200, 0)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50, "OPTIONS", BLUE, (0, 0, 200)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50, "QUIT", RED, (200, 0, 0))
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
            
            # Draw
            display_surface.fill(WHITE)
            
            # Draw title
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("THE DARK NIGHT", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            display_surface.blit(title_text, title_rect)
            
            # Draw buttons
            for button in self.buttons:
                button.draw(display_surface)
            
            pygame.display.update()
            clock.tick(FPS) 