from cities_game.game import Game
from cities_game.bot import Bot
import numpy as np

class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        game.logger.debug("Hello world")