from cities_game.city import City
from cities_game.capital_city import Capital
from cities_game.group import Group

class Player:
    def __init__(self, cities: list[City], capital_city: Capital | None, groups: list[Group]) -> None:
        self.cities = cities
        self.capital_city = capital_city
        self.groups = groups
        self.conquered_cities = []
        self.lost_cities = []

    def convert_actions(self, action):
        cities = self.cities + [self.capital_city]
        if action[0] not in cities:
            return None
        action[0] = cities.index(action[0])



    def update_groups(self) -> None:
        for group in self.groups:
            group.update()
            if group.turns_till_arrival == 0:
                if group.destination in self.cities or group.destination is self.capital_city:
                    group.destination.people_amount += group.people_amount
                else:
                    group.destination.people_amount -= group.people_amount
                    if group.destination.people_amount < 0:
                        self.conquered_cities.append(group.destination)
                self.groups.remove(group)

    def update_cities(self, actions) -> None:
        for city in self.cities:
            if city.people_amount < 0:
                self.lost_cities.append(city)
            else:
                city.update()
        for action in actions:
            try:
                cities = self.cities + [self.capital_city]
                city = cities[cities.index(action[0])]
                if action[1] == "upgrade":
                    if city.can_upgrade():
                        city.people_amount -= city.get_upgrade_cost()
                        city.level += 1
                elif action[1] == "send":
                    try:
                        if city.can_send_group(action[3]) and isinstance(action[2], City):
                            city.people_amount -= action[3]
                            self.groups.append(Group(action[3], city, action[2], city.position))
                    except Exception:
                        pass

            except ValueError:
                pass

        if self.capital_city is not None:
            if self.capital_city.people_amount < 0:
                self.capital_city = None
            else:
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

