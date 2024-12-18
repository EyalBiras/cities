import gzip
import json
from pathlib import Path

import pygame

from game_render.file_drawer import FileDrawer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 200, 0)
RED = (255, 0, 0)


class Menu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("File Menu")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((1920, 1080))
        self.clock = pygame.time.Clock()
        self.selected_game_file = None
        self.selected_log_file = None
        self.proceed = self.font.render(f"proceed", True, BLACK)
        self.proceed_button = pygame.Rect(0, 100, self.proceed.get_width(), self.proceed.get_height())
        self.id = None
        self.wrong_choice = False

    def render_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        return pygame.Rect(x, y, text_surface.get_width(), text_surface.get_height())

    def run(self):
        current_dir = Path(__file__).parent / "games"
        file_list = [FileDrawer(f) for f in current_dir.glob("*") if show_file(f)]
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(WHITE)
            self.display.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.proceed_button.collidepoint(mouse_pos) and self.selected_game_file:
                            return self.selected_game_file, self.selected_log_file
                        for f in file_list:
                            selected_file = f.is_clicked(mouse_pos)
                            if selected_file:
                                self.wrong_choice = False
                                if selected_file.name.endswith(".log"):
                                    print(extract_id_from_log(selected_file))
                                    print(self.id)
                                    if self.selected_log_file:
                                        self.selected_log_file = selected_file
                                        self.id = extract_id_from_gzip(selected_file)
                                        self.selected_game_file = None
                                    else:
                                        if self.id is None:
                                            self.selected_log_file = selected_file
                                            self.id = extract_id_from_log(selected_file)
                                        else:
                                            if self.id == extract_id_from_log(selected_file):
                                                self.selected_log_file = selected_file
                                            else:
                                                self.wrong_choice = True
                                elif selected_file.name.endswith(".json.gzip"):
                                    if self.selected_game_file:
                                        self.selected_game_file = selected_file
                                        self.id = extract_id_from_gzip(selected_file)
                                        self.selected_log_file = None
                                    else:
                                        if self.id is None:
                                            self.selected_game_file = selected_file
                                            self.id = extract_id_from_gzip(selected_file)
                                        else:
                                            if self.id == extract_id_from_gzip(selected_file):
                                                self.selected_game_file = selected_file
                                            else:
                                                self.wrong_choice = True
            y = 100
            for i, file in enumerate(file_list):
                color = BLACK
                y = file.draw(self.display, self.font, color, 50, y + 40)
            if self.selected_game_file:
                text_surface = self.font.render(f"Selected game file: {self.selected_game_file}", True, HIGHLIGHT_COLOR)
                self.display.blit(text_surface, (0, 0))
            if self.selected_log_file:
                text_surface = self.font.render(f"Selected log file: {self.selected_log_file}", True, HIGHLIGHT_COLOR)
                self.display.blit(text_surface, (0, 20))
            if self.wrong_choice:
                text_surface = self.font.render(f"You selected the wrong file! these files dont have a matching id!", True, RED)
                self.display.blit(text_surface, (0, 40))
            pygame.draw.rect(self.display, (100, 0, 200), self.proceed_button, 2)
            self.display.blit(self.proceed, (0, 100))

            self.clock.tick(60)
            self.screen.blit(self.display, (0, 0))
            pygame.display.flip()

def show_file(file: Path):
    if file.is_dir():
        return True
    return file.name.endswith(".json.gzip") or file.name.endswith(".log")

def extract_id_from_log(log_file: Path):
    with open(log_file, "r") as f:
        first_line = f.readline()
    return first_line[first_line.find("]") + 3:].replace("\n", "")

def extract_id_from_gzip(game_file: Path):
    with gzip.open(game_file, 'rt', encoding='utf-8') as file:
        loaded_data_t = json.load(file)
    return loaded_data_t["id"]

