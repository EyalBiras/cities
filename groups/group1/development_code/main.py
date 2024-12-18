from cities_game import Game, Group, Bot

class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        game.get_my_cities()[0].send_group(game.get_my_city_capital(), 3)
