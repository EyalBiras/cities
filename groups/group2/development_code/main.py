from cities_game.game import Game
from cities_game.bot import Bot

class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        game.logger.debug("hl")
        if game.get_my_city_capital().people_amount > 10:
            cities = [game.get_my_city_capital()]
            game.logger.debug("hello")
            for city in cities:
                city.send_group(game.get_enemy_city_capital(), game.get_my_city_capital().people_amount - 5)
                game.logger.debug("Sent")