import gzip
import json
from pathlib import Path
from map_editor.tile import Tile
import cv2
import numpy as np
from PIL import Image

from cities_game.capital_city import Capital
from cities_game.city import City
from cities_game.player import Player

WINDOW_SIZE = (1920, 1080)
FILE = Path(__file__)
MAP_FILE = FILE.parent / "map_editor" / "test.json"
def reset_game():
    with open(MAP_FILE) as f:
        game_map = json.load(f)

    neutral_cities = []
    for building_type, position in game_map["buildings"]:
        if building_type == Tile.CITY:
            neutral_cities.append(City(5, 1, np.array(position)))
        elif building_type == Tile.CAPITAL:
            if position[0] < WINDOW_SIZE[0] // 2:
                p1_capital = Capital(5, 1, np.array((position)))
            else:
                p2_capital = Capital(5, 1, np.array((position)))

    decorations = []
    for decoration, position in game_map["decorations"]:
        decorations.append((Image.open(decoration), position))
    p1 = Player(neutral_cities, p1_capital, [])
    p2 = Player([], p2_capital, [])
    neutral_player = Player([], None, [])
    print(p2_capital.position)
    return p1, p2, neutral_player, decorations


# def reset_game():
#     p1_capital = Capital(5, 1, np.array((150, WINDOW_SIZE[1] // 2)))
#     p2_capital = Capital(5, 1, np.array((WINDOW_SIZE[0] - 150, WINDOW_SIZE[1] // 2)))
#     p1_groups = []
#     p2_groups = []
#     neutral_cities = [City(5, 0, np.array((WINDOW_SIZE[0] // 4, WINDOW_SIZE[1] // 4))), City(5, 0, np.array((WINDOW_SIZE[0] // 4,  3 * WINDOW_SIZE[1] // 4))),
#                       City(5, 0, np.array((3 * WINDOW_SIZE[0] // 4, WINDOW_SIZE[1] // 4))), City(5, 0, np.array((3 * WINDOW_SIZE[0] // 4 , 3 * WINDOW_SIZE[1] // 4))),
#                       City(5, 0, np.array((WINDOW_SIZE[0] // 2, WINDOW_SIZE[0] // 2)))]
#     p1 = Player([], p1_capital, p1_groups)
#     p2 = Player([], p2_capital, p2_groups)
#     neutral_player = Player(neutral_cities, None, [])
#     return p1, p2, neutral_player


def images_to_video(image_objects: list[Image], output_video_path, fps=1, size=None) -> None:
    output_video_path = Path(output_video_path)
    output_video_path.parent.mkdir(parents=True, exist_ok=True)
    if not image_objects:
        raise ValueError("The list of image objects is empty.")

    if isinstance(image_objects[0], bytes):
        first_image = cv2.imdecode(np.frombuffer(image_objects[0], np.uint8), cv2.IMREAD_COLOR)
    else:
        first_image = np.array(image_objects[0])
        first_image = cv2.cvtColor(first_image, cv2.COLOR_RGB2BGR)

    if first_image is None:
        raise ValueError("Could not read the first image.")

    height, width, _ = first_image.shape
    if size is None:
        size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, size)

    for image_obj in image_objects:
        if isinstance(image_obj, bytes):
            img = cv2.imdecode(np.frombuffer(image_obj, np.uint8), cv2.IMREAD_COLOR)
        else:
            img = np.array(image_obj)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if img is None:
            print("Warning: Could not read an image. Skipping.")
            continue

        out.write(img)

    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved to: {output_video_path}")

import pickle

# Depickling (loading) the object from the file
# with open('test.pkl', 'rb') as file:
#     loaded_data = pickle.load(file)
#
# with gzip.open('data.json.gz', 'rt', encoding='utf-8') as file:
#     loaded_data_t = json.load(file)
#
# print(loaded_data[1] == loaded_data_t[1])
# print(loaded_data_t[2])
# print(loaded_data[2])
# # Apply the conversion to loaded_data_t
# print(loaded_data == loaded_data_t)
# print(loaded_data_t[1])
# print(loaded_data[1])