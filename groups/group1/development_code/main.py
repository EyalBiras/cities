from cities_game import Game, Group, Bot

class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        if game.get_my_city_capital().people_amount > 5:
            cities = game.get_my_cities() + [game.get_my_city_capital()]
            for city in cities:
                city.send_group(game.get_enemy_city_capital(), game.get_my_city_capital().people_amount - 5)