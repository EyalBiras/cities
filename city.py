from __future__ import annotations

from typing import Self


class City:
    def __init__(self, people_amount: int, level: int, position: tuple[int, int]) -> None:
        self.__people_amount = people_amount
        self.__level = level
        self.__action = None
        self.__position = position

    @property
    def people_amount(self):
        return self.__people_amount


    @property
    def position(self):
        return self.__position

    def get_turns_till_arrival(self, destination: City) -> int:
        return ((self.__position[0] - destination.position[0]) ** 2 + (self.__position[1] - destination.position[1]) ** 2)**0.5

    def can_send_groups(self, people_amount: int) -> bool:
        return people_amount < self.__people_amount

    def send_group(self, destination: Self, people_amount: int) -> None:
        if self.can_send_groups(people_amount):
            self.__action = ["send", self, destination, people_amount]

    def get_upgrade_cost(self) -> int:
        return 20

    def can_upgrade(self) -> bool:
        return self.get_upgrade_cost() < self.__people_amount and self.__level < 4

    def upgrade(self):
        if self.can_upgrade():
            self.__action = ["upgrade"]
