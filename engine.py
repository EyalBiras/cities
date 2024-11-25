from capital_city import Capital
from city import City
from group import Group
from player import Player
from PIL import Image, ImageDraw, ImageFont


class Engine:
    def __init__(self, player: Player, enemy: Player) -> None:
        self.player = player
        self.enemy = enemy
        self.winner = None
        self.turn = 1

    def update(self) -> None:
        self.player.update_groups()
        self.enemy.update_groups()
        self.player.update_cities()
        self.enemy.update_cities()
        self.player.update_lost_cities()
        self.enemy.update_lost_cities()
        self.player.update_conquered_cities()
        self.enemy.update_conquered_cities()
        if self.player.capital_city is None:
            self.winner = "enemy"
        elif self.enemy.capital_city is None:
            self.winner = "player"
        if self.turn == 300 and self.winner is None:
            if len(self.player.cities) > len(self.enemy.cities):
                self.winner = "player"
            elif len(self.enemy.cities) > len(self.player.cities):
                self.winner = "enemy"
            else:
                self.winner = "draw"
        self.turn += 1

    def draw_player(self,
                    player: Player,
                    draw: ImageDraw,
                    font: ImageFont,
                    city_color,
                    capital_color,
                    group_color) -> None:
        for city in player.cities:
            draw.rectangle([city.position[0], city.position[1], city.position[0] + 50, city.position[1] + 50],
                           outline=city_color, width=5)
            draw.text((city.position[0] + 20, city.position[1] + 20), f"{city.people_amount}", fill="black", font=font)
        for group in player.groups:
            draw.rectangle([group.position[0], group.position[1], group.position[0] + 10, group.position[1] + 10],
                           outline=group_color, width=5)
            draw.text((group.position[0], group.position[1]), f"{group.people_amount}", fill="cyan", font=font)
        capital = player.capital_city
        if capital:
            draw.rectangle([capital.position[0], capital.position[1], capital.position[0] + 50, capital.position[1] + 50],
                           outline=capital_color, width=10)
            draw.text((capital.position[0] + 20, capital.position[1] + 20), f"{capital.people_amount}", fill="black",
                      font=font)

    def draw(self) -> Image:
        image = Image.new('RGB', (1000, 1000), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        self.draw_player(self.player, draw, font, "blue", "yellow", "cyan")
        self.draw_player(self.enemy, draw, font, "red", "black", "pink")
        self.update()
        if self.winner is not None:
            font = ImageFont.load_default(100)
            draw.text((150, 250), f"{self.winner}", fill="black", font=font)

        return image

    def play(self) -> list[Image]:
        images = []
        while self.winner is None:
            images.append(self.draw())
        return images
