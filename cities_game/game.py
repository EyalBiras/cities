import logging

from cities_game.capital_city import Capital
from cities_game.city import City
from cities_game.group import Group
from cities_game.player import Player


class Game:
    def __init__(self, player: Player, enemy: Player, neutral: Player, turn: int, logger: logging.Logger) -> None:
        self.player = player
        self.enemy = enemy
        self.__neutral = neutral
        self.__turn = turn
        self.logger = logger

    def get_enemy_cities(self) -> list[City]:
        return self.enemy.cities

    def get_enemy_city_capital(self) -> Capital:
        return self.enemy.capital_city

    def get_enemy_groups(self) -> list[Group]:
        return self.enemy.groups

    def get_my_cities(self) -> list[City]:
        return self.player.cities

    def get_my_city_capital(self) -> Capital:
        return self.player.capital_city

    def get_my_groups(self) -> list[Group]:
        return self.player.groups

    def get_neutral_cities(self) -> list[City]:
        return self.__neutral.cities

    @property
    def turn(self):
        return self.__turn
