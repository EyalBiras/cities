from abc import ABC, abstractmethod
from game import Game

class Bot(ABC):
    @abstractmethod
    def do_turn(self, game: Game) -> None:
        pass