import pygame
from ui_components.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, WHITE, BLACK, FPS


class OptionsScreen:
    def __init__(self) -> None:
        self.back_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "BACK", BLUE, (0, 0, 200))
        
    def run(self, display_surface: pygame.Surface, clock: pygame.time.Clock) -> str:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                    
                if self.back_button.handle_event(event):
                    return "back"
            
            # Draw
            display_surface.fill(WHITE)
            
            # Draw title
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("OPTIONS", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            display_surface.blit(title_text, title_rect)
            
            # Draw options info
            info_font = pygame.font.Font(None, 36)
            info_text = [
                "Controls:",
                "Arrow Keys - Move Hero",
                "ESC, Tab, Backspace, Q - Quit Game",
                "",
                "Game runs in fullscreen mode only"
            ]
            
            for i, line in enumerate(info_text):
                text_surface = info_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 40))
                display_surface.blit(text_surface, text_rect)
            
            # Draw back button
            self.back_button.draw(display_surface)
            
            pygame.display.update()
            clock.tick(FPS) 