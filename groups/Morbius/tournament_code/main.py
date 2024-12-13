from cities_game.game import Game
from cities_game.bot import Bot
import numpy as np

class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        if game.get_my_city_capital().people_amount > 10:
            game.get_my_city_capital().send_group(game.get_enemy_city_capital(), game.get_my_city_capital().people_amount - 1)