import logging


class TurnFilter(logging.Filter):
    def __init__(self, turn) -> None:
        super().__init__()
        self.turn = turn

    def filter(self, record) -> bool:
        record.turn = self.turn
        return True
