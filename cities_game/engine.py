import copy
import time

from PIL import Image, ImageDraw, ImageFont
from cities_game.timeout import timeout
from cities_game.bot import Bot
from cities_game.city import City
from cities_game.game import Game
from cities_game.player import Player

TIME_LIMIT = 2


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
                 neutral: Player) -> None:
        self.player = player
        self.player_bot = player_bot
        self.player_name = player_name
        self.player_actions = []
        self.player_time = 0
        self.enemy = enemy
        self.enemy_bot = enemy_bot
        self.enemy_name = enemy_name
        self.enemy_actions = []
        self.enemy_time = 0
        self.neutral = neutral
        self.winner = None
        self.turn = 1

    def create_game_player(self) -> Game:
        return Game(copy.deepcopy(self.player), copy.deepcopy(self.enemy), copy.deepcopy(self.neutral))

    def create_game_enemy(self) -> Game:
        return Game(copy.deepcopy(self.enemy), copy.deepcopy(self.player), copy.deepcopy(self.neutral))

    def convert_city(self, city: City):
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

    def convert_action(self, action):
        action[0] = self.convert_city(action[0])
        if action[1] == "send":
            action[2] = self.convert_city(action[2])
        return action

    def do_turn(self) -> None:
        player_game = self.create_game_player()
        try:
            with timeout(TIME_LIMIT):
                t_start = time.perf_counter()
                self.player_bot.do_turn(player_game)
            t_end = time.perf_counter()
            self.player_time += t_end - t_start
            player_actions = [city.action for city in player_game.player.cities]
            player_actions.append(player_game.player.capital_city.action)
            self.player_actions = [self.convert_action(action) for action in player_actions if action is not None]
        except Exception as e:
            self.winner = "enemy"
            return

        enemy_game = self.create_game_enemy()
        try:
            with timeout(TIME_LIMIT):
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
        if self.turn == 300 and self.winner is None:
            if len(self.player.cities) > len(self.enemy.cities):
                self.winner = "player"
            elif len(self.enemy.cities) > len(self.player.cities):
                self.winner = "enemy"
            else:
                self.winner = "draw"
        self.turn += 1

    @staticmethod
    def draw_player(player: Player,
                    draw: ImageDraw,
                    font: ImageFont,
                    city_color,
                    capital_color,
                    group_color) -> None:
        for city in player.cities:
            draw.rectangle([city.position[0], city.position[1], city.position[0] + 50, city.position[1] + 50],
                           outline=city_color, width=5)
            draw.text((city.position[0] + 20, city.position[1] + 20), f"{city.people_amount}", fill="black", font=font)
        for group in player.groups:
            draw.rectangle([group.position[0], group.position[1], group.position[0] + 10, group.position[1] + 10],
                           outline=group_color, width=5)
            draw.text((group.position[0], group.position[1]), f"{group.people_amount}", fill="cyan", font=font)
        capital = player.capital_city
        if capital:
            draw.rectangle(
                [capital.position[0], capital.position[1], capital.position[0] + 50, capital.position[1] + 50],
                outline=capital_color, width=10)
            draw.text((capital.position[0] + 20, capital.position[1] + 20), f"{capital.people_amount}", fill="black",
                      font=font)

    def draw(self) -> Image:
        image = Image.new('RGB', (1000, 1000), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        names_font = ImageFont.truetype("arial.ttf", 30)
        draw.text((300, 50), f"{self.player_name}", fill="black", font=names_font)
        draw.text((300, 400), f"{self.enemy_name}", fill="black", font=names_font)
        self.draw_player(self.player, draw, font, "blue", "yellow", "cyan")
        self.draw_player(self.enemy, draw, font, "red", "black", "pink")
        self.draw_player(self.neutral, draw, font, "gray", "gray", "gray")
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
        return images, self.winner
