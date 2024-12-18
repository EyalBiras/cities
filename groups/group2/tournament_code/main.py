from cities_game import Bot, Game


class MyBot(Bot):
    def do_turn(self, game: Game) -> None:
        game.logger.debug("hi")
        print("hi")
        if game.get_my_city_capital().people_amount > 10:
            cities = [game.get_my_city_capital()]
            for city in cities:
                if game.turn % 2 == 0:
                    city.send_group(game.get_enemy_city_capital(), 3)
                    game.logger.debug("Sent")
                if game.turn % 2 == 1:
                    city.send_group(game.get_neutral_cities()[0], 1)
                    game.logger.debug("Sent")
