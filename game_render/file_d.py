from pathlib import Path

import pygame


class FileDrawer:
    def __init__(self, file: Path):
        self.file = file
        self.children = []
        self.rect = None

    def is_clicked(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            if self.file.is_dir():
                if len(self.children) == 0:
                    self.children = [FileDrawer(f) for f in self.file.glob("*")]
                else:
                    self.children = []
            else:
                return self.file
        else:
            for child in self.children:
                a = child.is_clicked(mouse_position)
                if a:
                    return a


    def draw(self,display, font, color, x, y):
        text_surface = font.render(self.file.name, True, color)
        display.blit(text_surface, (x, y))
        self.rect = pygame.Rect(x, y, text_surface.get_width(), text_surface.get_height())
        for i, child in enumerate(self.children):
            y = child.draw(display, font, color, x + 10, y + 40)
        return y



