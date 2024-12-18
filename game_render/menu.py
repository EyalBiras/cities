from pathlib import Path

import pygame

from game_render.file_d import FileDrawer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 200, 0)


class Menu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("File Menu")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((1920, 1080))
        self.clock = pygame.time.Clock()
        self.selected_file = None
        self.proceed = self.font.render(f"proceed", True, BLACK)
        self.proceed_button = pygame.Rect(0, 100, self.proceed.get_width(), self.proceed.get_height())

    def render_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        return pygame.Rect(x, y, text_surface.get_width(), text_surface.get_height())

    def run(self):
        current_dir = Path(__file__).parent
        file_list = [FileDrawer(f) for f in current_dir.glob("*")]
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(WHITE)
            self.display.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.proceed_button.collidepoint(mouse_pos) and self.selected_file:
                            return self.selected_file
                        for f in file_list:
                            selected_file = f.is_clicked(mouse_pos)
                            if selected_file:
                                self.selected_file = selected_file
            y = 100
            for i, file in enumerate(file_list):
                color = BLACK
                y = file.draw(self.display, self.font, color, 50, y + 40)
            if self.selected_file:
                text_surface = self.font.render(f"Selected file: {self.selected_file}", True, HIGHLIGHT_COLOR)
                self.display.blit(text_surface, (0, 0))
            pygame.draw.rect(self.display, (100, 0, 200), self.proceed_button, 2)
            self.display.blit(self.proceed, (0, 100))

            self.clock.tick(60)
            self.screen.blit(self.display, (0, 0))
            pygame.display.flip()
