import copy
import json
import logging
import logging.config
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from cities_game.bot import Bot
from cities_game.city import City
from cities_game.game import Game
from cities_game.images import ImagesType, player_type_to_images, TERRAIN_IMAGE, CITY_SIZE, CAPITAL_SIZE, \
    get_group_image, KNIGHT_SIZE
from cities_game.player import Player
from cities_game.player_type import PlayerType
from cities_game.timeout import timeout

LOG_CONFIGURATION_FILE = Path(__file__).parent / "log.json"
GROUPS_DIRECTORY = Path(__file__).parent.parent / "groups"
TIME_LIMIT = 2
WINDOW_SIZE = (1920, 1080)

def setup_logging(group: str, log_file: str, needs_logging=True) -> logging.Logger:
    logger = logging.getLogger(group)
    with open(LOG_CONFIGURATION_FILE, "r") as f:
        configuration = json.load(f)
    if not needs_logging:
        logger.addHandler(logging.NullHandler())
    else:
        configuration["handlers"]["file"]["filename"] = log_file
        configuration["loggers"][group] = {
            "level": "DEBUG",
            "handlers": [
                "file",
                "stderr"
            ]
        }
    logging.config.dictConfig(configuration)
    return logger


class CityNotFoundERROR(Exception):
    pass


class Engine:
    def __init__(self,
                 player: Player,
                 player_bot: Bot,
                 player_name: str,
                 enemy: Player,
                 enemy_bot: Bot,
                 enemy_name: str,
                 neutral: Player,
                 decorations: list[Image, tuple[int, int]],
                 is_tournament: bool = True
                 ) -> None:
        self.player = player
        self.player_bot = player_bot
        self.player_name = player_name
        self.player_actions = []
        self.player_time = 0
        self.player_log_file = GROUPS_DIRECTORY / player_name / "battles" / enemy_name / "battle.log"
        self.player_log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.player_log_file, "w") as f:
            pass
        self.player_logger = setup_logging(player_name, str(self.player_log_file), not is_tournament)

        self.enemy = enemy
        self.enemy_bot = enemy_bot
        self.enemy_name = enemy_name
        self.enemy_actions = []
        self.enemy_time = 0
        self.enemy_log_file = GROUPS_DIRECTORY / enemy_name / "battles" / player_name / "battle.log"
        self.enemy_log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.enemy_log_file, "w") as f:
            pass
        self.enemy_logger = setup_logging(enemy_name, str(self.enemy_log_file), False)

        self.neutral = neutral
        self.winner = None
        self.turn = 1
        self.decorations = decorations
        self.is_tournament = is_tournament

    def create_game_player(self) -> Game:
        return Game(copy.deepcopy(self.player), copy.deepcopy(self.enemy), copy.deepcopy(self.neutral), self.turn,
                    self.player_logger)

    def create_game_enemy(self) -> Game:
        return Game(copy.deepcopy(self.enemy), copy.deepcopy(self.player), copy.deepcopy(self.neutral), self.turn,
                    self.enemy_logger)

    def convert_city(self, city: City) -> City:
        cities = self.player.cities + [self.player.capital_city]
        if city in cities:
            return cities[cities.index(city)]
        cities = self.enemy.cities + [self.enemy.capital_city]
        if city in cities:
            return cities[cities.index(city)]
        cities = self.neutral.cities
        if city in cities:
            return cities[cities.index(city)]
        raise CityNotFoundERROR()

    def convert_action(self, action) -> list[str]:
        action[0] = self.convert_city(action[0])
        if action[1] == "send":
            action[2] = self.convert_city(action[2])
        return action

    def do_turn(self) -> None:
        player_game = self.create_game_player()
        try:
            with timeout(TIME_LIMIT + 1000):
                t_start = time.perf_counter()
                self.player_bot.do_turn(player_game)
            t_end = time.perf_counter()
            self.player_time += t_end - t_start
            player_actions = [city.action for city in player_game.player.cities]
            player_actions.append(player_game.player.capital_city.action)
            self.player_actions = [self.convert_action(action) for action in player_actions if action is not None]
        except Exception as e:
            self.winner = "enemy"
            self.player_logger.exception("An error occurred")
            return

        enemy_game = self.create_game_enemy()

        try:
            with timeout(TIME_LIMIT + 1000):
                t_start = time.perf_counter()
                self.enemy_bot.do_turn(enemy_game)
            t_end = time.perf_counter()
            self.enemy_time += t_end - t_start
            enemy_actions = [city.action for city in enemy_game.player.cities]
            enemy_actions.append(enemy_game.player.capital_city.action)
            self.enemy_actions = [self.convert_action(action) for action in enemy_actions if action is not None]
        except Exception as e:
            self.winner = "player"
            return

    def update(self) -> None:
        self.do_turn()

        self.player.update_groups()
        self.enemy.update_groups()
        self.player.update_cities(self.player_actions)
        self.enemy.update_cities(self.enemy_actions)
        self.neutral.update_cities([])
        self.player.update_lost_cities()
        self.enemy.update_lost_cities()
        self.neutral.update_lost_cities()
        self.player.update_conquered_cities()
        self.enemy.update_conquered_cities()

        if self.player.capital_city is None or self.player_time > TIME_LIMIT:
            self.winner = "enemy"
            if self.enemy.capital_city is None or self.enemy_time > TIME_LIMIT:
                self.winner = "draw"
        elif self.enemy.capital_city is None or self.enemy_time > TIME_LIMIT:
            self.winner = "player"
        if self.turn == 100 and self.winner is None:
            if len(self.player.cities) > len(self.enemy.cities):
                self.winner = "player"
            elif len(self.enemy.cities) > len(self.player.cities):
                self.winner = "enemy"
            else:
                self.winner = "draw"
        self.turn += 1

    @staticmethod
    def draw_player(player: Player,
                    image: Image,
                    draw: ImageDraw,
                    font: ImageFont,
                    kind: PlayerType,
                    group_color) -> None:

        for city in player.cities:
            city_image = player_type_to_images[kind][ImagesType.CITY]
            image.paste(city_image, (int(city.position[0]) - CITY_SIZE[0] // 2, int(city.position[1]) - CITY_SIZE[1] // 2),
                        city_image.getchannel('A'))
            draw.text((city.position[0], city.position[1] - CITY_SIZE[1]//2), f"{city.people_amount}", fill=group_color,
                      font=font)
        for group in player.groups:
            group_image = get_group_image(kind, group.people_amount)[group.animation_phase]
            image.paste(group_image, (int(group.position[0]), int(group.position[1])),
                        group_image.getchannel('A'))
            draw.text((group.position[0] + group_image.size[0] // 2, group.position[1] - KNIGHT_SIZE[1] // 2), f"{group.people_amount}", fill=group_color,
                      font=font)
        capital = player.capital_city
        if capital:
            capital_city_image = player_type_to_images[kind][ImagesType.CAPITAL]
            image.paste(capital_city_image, (int(capital.position[0]) - CAPITAL_SIZE[0] // 2, int(capital.position[1]) - CAPITAL_SIZE[1] // 2),
                        capital_city_image.getchannel('A'))
            draw.text((capital.position[0], capital.position[1] - CAPITAL_SIZE[0] // 2), f"{capital.people_amount}", fill=group_color,
                      font=font)

    def draw_decoration(self, image: Image):
        for decoration, position in self.decorations:
            image.paste(decoration, position, decoration.getchannel('A'))

    def draw(self) -> Image:
        image = Image.new('RGB', WINDOW_SIZE)
        for x in range(0, WINDOW_SIZE[0], TERRAIN_IMAGE.width):
            for y in range(0, WINDOW_SIZE[1], TERRAIN_IMAGE.height):
                image.paste(TERRAIN_IMAGE, (x, y))
        image = image.filter(ImageFilter.GaussianBlur(1))
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default(size=20)
        names_font = ImageFont.load_default(size=30)
        draw.text((0, 0), f"{self.player_name}", fill="black", font=names_font)
        text_box = names_font.getbbox(self.enemy_name)
        text_width = text_box[2] - text_box[0]
        draw.text((WINDOW_SIZE[0] - text_width, 0), f"{self.enemy_name}", fill="black", font=names_font)
        self.draw_player(self.player, image, draw, font, PlayerType.PLAYER, "blue")
        self.draw_player(self.enemy, image, draw, font, PlayerType.ENEMY, "red")
        self.draw_player(self.neutral, image, draw, font, PlayerType.NEUTRAL, "black")
        self.draw_decoration(image)
        self.update()
        if self.winner is not None:
            font = ImageFont.load_default(100)
            if self.winner == "player":
                self.winner = self.player_name
                draw.text((150, 250), f"{self.player_name} won", fill="black", font=font)
            elif self.winner == "enemy":
                self.winner = self.enemy_name
                draw.text((150, 250), f"{self.enemy_name} won", fill="black", font=font)
            else:
                draw.text((150, 250), f"draw", fill="black", font=font)

        return image

    def play(self) -> tuple[list[Image], str | None]:
        images = []
        while self.winner is None:
            images.append(self.draw())

        logging.shutdown()
        return images, self.winner
