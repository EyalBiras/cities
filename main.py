import cv2
import numpy as np
from time import perf_counter
from capital_city import Capital
from city import City
from engine import Engine
from game import Game
from group import Group
from player import Player
from bot import Bot

def images_to_video_from_objects(image_objects, output_video_path, fps=1, size=None):
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

        img_resized = cv2.resize(img, size)

        out.write(img_resized)

    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved to: {output_video_path}")

t1 = perf_counter()
p1_cities = [City(5,1, np.array((100,100))), City(5,1, np.array((200,100))), City(5,1, np.array((300,100)))]
p2_cities = [City(5,1, np.array((100,300))), City(5,1, np.array((200,300))), City(5,1, np.array((300,300)))]
p1_capital = Capital(5,1,np.array((0,100)))
p2_capital = Capital(5,1,np.array((0,300)))
p1_groups = []
p2_groups = []
class M(Bot):
    def do_turn(self, game: Game) -> None:
        if game.get_my_city_capital().people_amount > 10:
            cities = game.get_my_cities() + [game.get_my_city_capital()]
            for city in cities:
                city.send_group(game.get_enemy_city_capital(), game.get_my_city_capital().people_amount - 5)

class G(Bot):
    def do_turn(self, game: Game) -> None:
        if game.get_my_city_capital().people_amount > 2:
            cities = game.get_my_cities() + [game.get_my_city_capital()]
            for city in cities:
                city.send_group(game.get_enemy_city_capital(), game.get_my_city_capital().people_amount - 1)


p1 = Player(p1_cities, p1_capital, p1_groups)
p2 = Player(p2_cities, p2_capital, p2_groups)
m = M()
g = G()
e = Engine(p1,m, p2,m)
i = e.play()
images_to_video_from_objects(i, "a.mp4")
print(perf_counter() - t1)