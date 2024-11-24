from city import City

class Group:
    def __init__(self, people_amount: int, source: City, destination: City, turns_till_arrival: int, position: tuple[int, int]) -> None:
        self.people_amount = people_amount
        self.source = source
        self.destination = destination
        self.turns_till_arrival = turns_till_arrival
        self.__position = position

    @property
    def position(self):
        return self.__position

