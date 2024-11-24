from capital_city import Capital
from city import City
from group import Group
from player import Player
from PIL import Image, ImageDraw, ImageFont


class Engine:
    def __init__(self, player: Player, enemy: Player) -> None:
        self.player = player
        self.enemy = enemy

    def draw(self) -> Image:
        image = Image.new('RGB', (1000, 1000), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        for city in self.player.cities:
            draw.rectangle([city.position[0], city.position[1], city.position[0] + 50, city.position[1] + 50], outline="blue", width=5)
            draw.text((city.position[0] + 20, city.position[1] + 20), f"{city.people_amount}", fill="black", font=font)
        for group in self.player.groups:
            draw.rectangle([group.position[0], group.position[1], group.position[0] + 10, group.position[1] + 10],
                           outline="cyan", width=5)
            draw.text((group.position[0], group.position[1]), f"{group.people_amount}", fill="cyan", font=font)
        capital = self.player.capital_city
        draw.rectangle([capital.position[0], capital.position[1], capital.position[0] + 50, capital.position[1] + 50], outline="yellow", width=10)
        draw.text((capital.position[0] + 20, capital.position[1] + 20), f"{capital.people_amount}", fill="black", font=font)

        for city in self.enemy.cities:
            draw.rectangle([city.position[0], city.position[1], city.position[0] + 50, city.position[1] + 50], outline="red", width=5)
            draw.text((city.position[0] + 20, city.position[1] + 20), f"{city.people_amount}", fill="black", font=font)

        for group in self.enemy.groups:
            draw.rectangle([group.position[0], group.position[1], group.position[0] + 10, group.position[1] + 10],
                           outline="pink", width=5)
            draw.text((group.position[0], group.position[1]), f"{group.people_amount}", fill="pink", font=font)

        capital = self.enemy.capital_city
        draw.rectangle([capital.position[0], capital.position[1], capital.position[0] + 50, capital.position[1] + 50], outline="black", width=10)
        draw.text((capital.position[0] + 20, capital.position[1] + 20), f"{capital.people_amount}", fill="black", font=font)

        return image
