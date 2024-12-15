import gzip
import json
import sys
import time
from pathlib import  Path

import numpy as np
import pygame
from PIL import Image, ImageFilter

from cities_game.images import DECORATIONS_DIRECTORY, NEUTRAL_CAPITAL_FILE, NEUTRAL_CITY_FILE, TERRAIN_FILE,get_group_image
from map_editor.editor import load_images, load_image

FILE = Path(__file__)




def apply_gaussian_blur(pygame_surface):
    arr = pygame.surfarray.array3d(pygame_surface)
    pil_image = Image.fromarray(np.transpose(arr, (1, 0, 2)))

    pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=0.5))

    arr = np.array(pil_image)
    pygame_surface = pygame.surfarray.make_surface(np.transpose(arr, (1, 0, 2)))

    return pygame_surface

class GameRender:
    def __init__(self, game):
        pygame.display.set_caption("Map Editor")
        self.font = pygame.font.SysFont(None, 36)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((1920, 1080))
        self.clock = pygame.time.Clock()
        self.game = game
        self.assets = [load_images(DECORATIONS_DIRECTORY),
                       [load_image(NEUTRAL_CAPITAL_FILE), load_image(NEUTRAL_CITY_FILE)]]
        self.fps = 6
        self.previous = time.perf_counter()
        self.turn = 0
        self.background = pygame.Surface((1920, 1080))
        image = pygame.image.load(TERRAIN_FILE).convert()
        image.set_colorkey((0, 0, 0))
        for x in range(0, 1920, image.width):
            for y in range(0, 1080, image.height):
                self.background.blit(image, (x, y))
        self.background = apply_gaussian_blur(self.background)
        self.back = self.font.render(f"Back", True, (0, 0, 0))
        self.back_button = pygame.Rect(0, 100, self.back.get_width(), self.back.get_height())

    def render_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, (x, y))

    def render_turn(self):
        self.display.fill((0, 0, 0))
        turn = self.game[self.turn]
        self.display.blit(self.background)
        pygame.draw.rect(self.display, (100, 0, 200), self.back_button, 2)
        self.display.blit(self.back, (0, 100))
        self.render_text(f"FPS: {self.fps}, current turn :{self.turn}", 1920 // 2, 0, (255, 255, 255))
        for p, t in turn.items():
            for city in t["cities"]:
                city_image = self.assets[1][1]
                city_position = city[2]
                size = city_image.size
                self.display.blit(city_image,  (int(city_position[0]) - size[0] // 2, int(city_position[1]) - size[1] // 2))
            if p != "neutral":
                capital_image = self.assets[1][0]
                capital_position = t["capital"][0][2]
                size = capital_image.size
                self.display.blit(self.assets[1][0],(int(capital_position[0]) - size[0] // 2, int(capital_position[1]) - size[1] // 2))
                for group in t["groups"]:
                    group_image = get_group_image("Player", group[0])[0]
                    group_image = pygame.image.fromstring(group_image.tobytes(), group_image.size, "RGBA")
                    self.display.blit(group_image, group[1])

    def run(self):
        while True:

            if time.perf_counter() - self.previous > 1 / self.fps:
                self.render_turn()
                self.previous = time.perf_counter()
                self.turn += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.fps += 1
                        self.fps %= 60
                    if event.key == pygame.K_DOWN:
                        self.fps -= 1
                        if self.fps <= 0:
                            self.fps = 1
                    if event.key == pygame.K_RIGHT:
                        self.turn += self.fps
                    if event.key == pygame.K_LEFT:
                        self.turn -= self.fps
                        if self.turn < 0:
                            self.turn = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.back_button.collidepoint(pygame.mouse.get_pos()):
                            return

            self.screen.blit(self.display)

            pygame.display.update()
            self.clock.tick(60)

