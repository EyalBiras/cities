from pathlib import Path

import numpy as np
import pygame
from PIL import Image, ImageFilter
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

HIGHLIGHT_COLOR = (255, 200, 0)
IMAGES_BASE_FILE = Path(__file__).parent.parent / "Tiny Swords" / "Tiny Swords (Update 010)"
DECORATIONS_DIRECTORY = IMAGES_BASE_FILE / "Deco"
RESOURCES_DIRECTORY = IMAGES_BASE_FILE / "Resources"

TERRAIN_FILE = IMAGES_BASE_FILE / "Terrain" / "Ground" / "green_tile.png"
ASSETS_BASE_FILE = IMAGES_BASE_FILE / "Factions" / "Knights"

PLAYER_CITY_FILE = ASSETS_BASE_FILE / "Buildings" / "Tower" / "Tower_Blue.png"
PLAYER_CAPITAL_FILE = ASSETS_BASE_FILE / "Buildings" / "Castle" / "Castle_Blue.png"
PLAYER_KNIGHT_FILE = ASSETS_BASE_FILE / "Troops" / "Warrior" / "Blue"

ENEMY_CITY_FILE = ASSETS_BASE_FILE / "Buildings" / "Tower" / "Tower_Red.png"
ENEMY_CAPITAL_FILE = ASSETS_BASE_FILE / "Buildings" / "Castle" / "Castle_Red.png"
ENEMY_KNIGHT_FILE = ASSETS_BASE_FILE / "Troops" / "Warrior" / "Red"

NEUTRAL_CITY_FILE = ASSETS_BASE_FILE / "Buildings" / "Tower" / "Tower_yellow.png"
NEUTRAL_CAPITAL_FILE = ASSETS_BASE_FILE / "Buildings" / "Castle" / "Castle_yellow.png"

def load_image(image_path: Path, size: tuple[int, int] | None = None, reflect: bool = False):
    image = pygame.image.load(image_path).convert_alpha()
    image.set_colorkey((0, 0, 0))
    if size is not None:
        image = pygame.transform.scale(image, size)
    if reflect:
        image = pygame.transform.flip(image, True, False)
    return image


def load_images(images_directory: Path, size: tuple[int, int] | None = None):
    images = []
    for image_path in images_directory.glob("*"):
        images.append(load_image(image_path, size))
    return images


def load_decoration(decoration_directory: Path):
    images = []
    for image_path in decoration_directory.glob("*"):
        images.append(image_path)
    return images


def apply_gaussian_blur(pygame_surface):
    arr = pygame.surfarray.array3d(pygame_surface)
    pil_image = Image.fromarray(np.transpose(arr, (1, 0, 2)))

    pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=0.5))

    arr = np.array(pil_image)
    pygame_surface = pygame.surfarray.make_surface(np.transpose(arr, (1, 0, 2)))

    return pygame_surface


def concat_horizontally(image: pygame.Surface, count: int) -> pygame.Surface:
    if image.get_alpha() is None:
        image = image.convert_alpha()
    width, height = image.get_width(), image.get_height()

    new_width = width * count
    new_height = height

    new_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)

    for i in range(count):
        new_surface.blit(image, (i * width, 0))

    return new_surface


def concat_vertically(image: pygame.Surface, count: int) -> pygame.Surface:
    if image.get_alpha() is None:
        image = image.convert_alpha()
    width, height = image.get_width(), image.get_height()
    new_width = width
    new_height = height * count
    new_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
    for i in range(count):
        new_surface.blit(image, (0, i * height))
    return new_surface

def make_group(image: pygame.Surface, count: int) -> pygame.Surface:
    if count == 1:
        return image
    if count == 2:
        return concat_horizontally(image, 2)
    if count == 3:
        width, height = image.get_width(), image.get_height()
        new_width = width * 2
        new_height = height * 2
        concat_image = concat_horizontally(image, 2)
        new_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
        new_surface.blit(concat_image, (0, height))
        new_surface.blit(image, (width // 2, 0))
        return new_surface
    if count == 4:
        return concat_vertically(concat_horizontally(image, 2), 2)
    if count == 5:
        width, height = image.get_width(), image.get_height()
        new_width = width * 3
        new_height = height * 2
        concat_image = make_group(image, 4)
        new_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
        new_surface.blit(concat_image, (0, 0))
        new_surface.blit(image, (width * 2, height // 2))
        return new_surface
    if count == 6:
        return concat_vertically(concat_horizontally(image, 3), 2)


def get_knight(image_file: Path, size: tuple[int, int] | None = None, reflect: bool = False, count: int = 1) -> list[
    Image]:
    animation = []
    for warrior_image in image_file.glob("*"):
        if "Warrior_walk_animation" in warrior_image.name:
            animation.append(make_group(load_image(warrior_image, size, reflect), count=count))
    return animation


def get_group_image(kind: str, people_amount: int, reflect: bool = False):
    KNIGHT_SIZE = (
    int(get_knight(PLAYER_KNIGHT_FILE)[0].size[0] // 2), int(get_knight(PLAYER_KNIGHT_FILE)[1].size[1] // 2))
    if people_amount > 5:
        people_amount = 5
    if kind == "player":
        return get_knight(PLAYER_KNIGHT_FILE, KNIGHT_SIZE, reflect, people_amount)
    return get_knight(ENEMY_KNIGHT_FILE, KNIGHT_SIZE, reflect, people_amount)