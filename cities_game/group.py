from cities_game.city import City
import numpy as np

class Group:
    def __init__(self, people_amount: int, source: City, destination: City, position: np.ndarray[int]) -> None:
        self.people_amount = people_amount
        self.source = source
        self.destination = destination
        self.turns_till_arrival = self.source.get_turns_till_arrival(destination)
        self.__position = list(position)
        self.speed = 20
        self.__direction = (self.destination.position - self.source.position) / self.source.get_distance_to(destination)


    @property
    def position(self):
        return self.__position

    def update(self) -> None:
        self.turns_till_arrival -= 1
        self.__position += self.__direction * self.speed


