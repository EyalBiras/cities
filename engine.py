from webbrowser import Galeon
import copy

from wheel.cli.convert import convert

from capital_city import Capital
from city import City
from game import Game
from group import Group
from player import Player
from PIL import Image, ImageDraw, ImageFont
from bot import Bot

class Engine:
    def __init__(self, player: Player,player_bot: Bot, enemy: Player, enemy_bot: Bot) -> None:
        self.player = player
        self.player_bot = player_bot
        self.player_actions = []
        self.enemy = enemy
        self.enemy_bot = enemy_bot
        self.enemy_actions = []
        self.winner = None
        self.turn = 1

    def create_game_player(self) -> Game:
        return Game(copy.deepcopy(self.player), copy.deepcopy(self.enemy))

    def create_game_enemy(self) -> Game:
        return Game(copy.deepcopy(self.enemy), copy.deepcopy(self.player))

    def convert_city(self, city: City):
        cities = self.player.cities + [self.player.capital_city]
        if city in cities:
            return cities[cities.index(city)]
        cities = self.enemy.cities + [self.enemy.capital_city]
        if city in cities:
            return cities[cities.index(city)]

    def convert_action(self, action):
        action[0] = self.convert_city(action[0])
        if action[1] == "send":
            action[2] = self.convert_city(action[2])
        return action


    def do_turn(self) -> None:
        player_game = self.create_game_player()
        self.player_bot.do_turn(player_game)
        player_actions = [city.action for city in player_game.player.cities]
        player_actions.append(player_game.player.capital_city.action)
        self.player_actions = [self.convert_action(action) for action in player_actions if action is not None]

        enemy_game = self.create_game_enemy()
        self.enemy_bot.do_turn(enemy_game)
        enemy_actions = [city.action for city in enemy_game.player.cities]
        enemy_actions.append(enemy_game.player.capital_city.action)
        self.enemy_actions = [self.convert_action(action) for action in enemy_actions if action is not None]

    def update(self) -> None:
        self.do_turn()

        self.player.update_groups()
        self.enemy.update_groups()
        self.player.update_cities(self.player_actions)
        self.enemy.update_cities(self.enemy_actions)
        self.player.update_lost_cities()
        self.enemy.update_lost_cities()
        self.player.update_conquered_cities()
        self.enemy.update_conquered_cities()

        if self.player.capital_city is None:
            self.winner = "enemy"
            if self.enemy.capital_city is None:
                self.winner = "draw"
        elif self.enemy.capital_city is None:
            self.winner = "player"
        if self.turn == 300 and self.winner is None:
            if len(self.player.cities) > len(self.enemy.cities):
                self.winner = "player"
            elif len(self.enemy.cities) > len(self.player.cities):
                self.winner = "enemy"
            else:
                self.winner = "draw"
        self.turn += 1

    def draw_player(self,
                    player: Player,
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
            draw.rectangle([capital.position[0], capital.position[1], capital.position[0] + 50, capital.position[1] + 50],
                           outline=capital_color, width=10)
            draw.text((capital.position[0] + 20, capital.position[1] + 20), f"{capital.people_amount}", fill="black",
                      font=font)

    def draw(self) -> Image:
        image = Image.new('RGB', (1000, 1000), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        self.draw_player(self.player, draw, font, "blue", "yellow", "cyan")
        self.draw_player(self.enemy, draw, font, "red", "black", "pink")
        self.update()
        if self.winner is not None:
            font = ImageFont.load_default(100)
            draw.text((150, 250), f"{self.winner}", fill="black", font=font)

        return image

    def play(self) -> list[Image]:
        images = []
        while self.winner is None:
            images.append(self.draw())
        return images
