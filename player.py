from city import City
from capital_city import Capital
from group import Group

class Player:
    def __init__(self, cities: list[City], capital_city: Capital, groups: list[Group]) -> None:
        self.cities = cities
        self.capital_city = capital_city
        self.groups = groups
