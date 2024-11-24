from city import City

class Capital(City):
    def __init__(self, people_amount: int, level: int, position: tuple[int, int]) -> None:
        super().__init__(people_amount, level, position)