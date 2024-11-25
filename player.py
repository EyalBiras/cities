from city import City
from capital_city import Capital
from group import Group

class Player:
    def __init__(self, cities: list[City], capital_city: Capital, groups: list[Group]) -> None:
        self.cities = cities
        self.capital_city = capital_city
        self.groups = groups
        self.conquered_cities = []
        self.lost_cities = []

    def update_groups(self) -> None:
        for group in self.groups:
            group.update()
            if group.turns_till_arrival == 0:
                if group.destination in self.cities:
                    group.destination.people_amount += group.people_amount
                else:
                    group.destination.people_amount -= group.people_amount
                    if group.destination.people_amount < 0:
                        self.conquered_cities.append(group.destination)
                self.groups.remove(group)

    def update_cities(self) -> None:
        for city in self.cities:
            if city.people_amount < 0:
                self.lost_cities.append(city)
            else:
                city.update()
        self.capital_city.update()

    def update_lost_cities(self) -> None:
        for city in self.lost_cities:
            self.cities.remove(city)
        self.lost_cities = []


    def update_conquered_cities(self):
        for city in self.conquered_cities:
            city.people_amount *= -1
            self.cities.append(city)
        self.conquered_cities = []

