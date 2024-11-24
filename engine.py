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
        image = Image.new('RGB', (400, 400), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        for city in self.player.cities:
            draw.rectangle([city.position[0], city.position[1], city.position[0] + 10, city.position[1] + 10], outline="blue", width=5)
            draw.text((city.position[0], city.position[1]), f"{city.people_amount}", fill="black", font=font)
        capital = self.player.capital_city
        draw.rectangle([capital.position[0], capital.position[1], capital.position[0] + 10, capital.position[1] + 10], outline="yellow", width=10)
        draw.text((capital.position[0], capital.position[1]), f"{capital.people_amount}", fill="black", font=font)

        for city in self.enemy.cities:
            draw.rectangle([city.position[0], city.position[1], city.position[0] + 10, city.position[1] + 10], outline="red", width=5)
            draw.text((city.position[0], city.position[1]), f"{city.people_amount}", fill="black", font=font)
        capital = self.enemy.capital_city
        draw.rectangle([capital.position[0], capital.position[1], capital.position[0] + 10, capital.position[1] + 10], outline="black", width=10)
        draw.text((capital.position[0], capital.position[1]), f"{capital.people_amount}", fill="black", font=font)

        return image
