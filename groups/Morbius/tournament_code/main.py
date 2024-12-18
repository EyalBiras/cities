
import numpy as np
import numpy.random as r
from cities_game import Bot, Game


class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        game.logger.debug("Hello world")