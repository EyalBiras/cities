import logging

from cities_game.capital_city import Capital
from cities_game.city import City
from cities_game.group import Group
from cities_game.player import Player
from cities_game.turn_filter import TurnFilter


class Game:
    def __init__(self, player: Player, enemy: Player, neutral: Player, turn: int, logger: logging.Logger) -> None:
        self.__player = player
        self.__enemy = enemy
        self.__neutral = neutral
        self.__turn = turn
        self.__logger = logger
        self.__logger.addFilter(TurnFilter(self.__turn))

    @property
    def logger(self) -> logging.Logger:
        return self.__logger

    @property
    def enemy(self) -> Player:
        return self.__enemy

    @property
    def player(self) -> Player:
        return self.__player

    def get_enemy_cities(self) -> list[City]:
        return self.__enemy.cities

    def get_enemy_city_capital(self) -> Capital:
        return self.__enemy.capital_city

    def get_enemy_groups(self) -> list[Group]:
        return self.__enemy.groups

    def get_my_cities(self) -> list[City]:
        return self.__player.cities

    def get_my_city_capital(self) -> Capital:
        return self.__player.capital_city

    def get_my_groups(self) -> list[Group]:
        return self.__player.groups

    def get_neutral_cities(self) -> list[City]:
        return self.__neutral.cities

    @property
    def turn(self) -> int:
        return self.__turn
