from cities_game.game import Game
from cities_game.bot import Bot

class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        for city in game.get_my_cities():
            city.send_group(game.get_my_city_capital(), 1)