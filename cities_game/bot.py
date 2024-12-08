from abc import ABC

from cities_game.game import Game
from cities_game.timeout import timeout

TIME_LIMIT = 2


class Bot(ABC):
    @timeout(TIME_LIMIT)
    def do_turn(self, game: Game) -> None:
        pass
