from __future__ import annotations

import numpy as np


class City:
    def __init__(self, people_amount: int, level: int, position: np.ndarray[float]) -> None:
        self.__people_amount = people_amount
        self.__level = level
        self.__action = None
        self.__position = position.astype(float)

    @property
    def level(self) -> int:
        return self.__level

    @level.setter
    def level(self, value: int) -> None:
        level = value

    @property
    def action(self):
        return self.__action

    @property
    def people_amount(self) -> int:
        return self.__people_amount

    @people_amount.setter
    def people_amount(self, value: int) -> None:
        self.__people_amount = value

    @property
    def position(self) -> np.ndarray[float]:
        return self.__position

    def get_distance_to(self, destination: City) -> float:
        return float(np.linalg.norm(destination.position - self.position))

    def get_turns_till_arrival(self, destination: City) -> int:
        return np.ceil(self.get_distance_to(destination) / 40)

    def can_send_group(self, people_amount: int) -> bool:
        return people_amount < self.__people_amount

    def send_group(self, destination: City, people_amount: int) -> None:
        if self.can_send_group(people_amount):
            self.__action = [self, "send", destination, people_amount]

    def get_upgrade_cost(self) -> int:
        return self.__level * 30

    def can_upgrade(self) -> bool:
        return self.get_upgrade_cost() < self.__people_amount and self.__level < 4

    def upgrade(self) -> None:
        if self.can_upgrade():
            self.__action = [self, "upgrade"]

    def update(self) -> None:
        self.__people_amount += self.__level

    def __eq__(self, other: City) -> bool:
        return np.array_equal(self.position, other.position)
