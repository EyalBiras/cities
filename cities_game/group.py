from functools import lru_cache

import numpy as np

from cities_game.city import City
from cities_game.update_flag import internal_update_flag


class Group:
    def __init__(self, people_amount: int, source: City, destination: City, position: np.ndarray[float]) -> None:
        self.__people_amount = people_amount
        self.__source = source
        self.__destination = destination
        self.__turns_till_arrival = self.__source.get_turns_till_arrival(destination)
        self.__position = position.astype(float)
        self.__speed = 40
        self.__velocity = self.__calculate_velocity(source, destination, self.__speed)
        self.__animation_phase = 0

    @property
    def animation_phase(self) -> int:
        return self.__animation_phase

    @property
    def speed(self) -> float:
        return self.__speed

    @property
    def turns_till_arrival(self) -> int:
        return self.__turns_till_arrival

    @property
    def destination(self) -> City:
        return self.__destination

    @property
    def source(self) -> City:
        return self.__source

    @property
    def people_amount(self) -> int:
        return self.__people_amount

    @staticmethod
    @lru_cache(maxsize=64)
    def __calculate_velocity(source: City, destination: City, speed: int):
        direction = (destination.position - source.position) / source.get_distance_to(destination)
        return direction * speed

    @property
    def position(self) -> np.ndarray[float]:
        return self.__position

    def update(self) -> None:
        if internal_update_flag.is_allowed():
            self.__turns_till_arrival -= 1
            self.__position += self.__velocity
            self.__animation_phase += 1
            self.__animation_phase %= 6
