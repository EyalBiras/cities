from capital_city import Capital
from city import City
from group import Group
from player import Player

class Game:
    def __init__(self, player: Player, enemy: Player) -> None:
        self.player = player
        self.enemy = enemy

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
        pass