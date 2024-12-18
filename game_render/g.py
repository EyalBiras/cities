import gzip
import json

import pygame
from r import GameRender
from menu import Menu



class A:
    def __init__(self):
        pygame.init()

    def run(self):
        while True:
            m = Menu()
            game_file, log_file = m.run()
            with gzip.open(game_file, 'rt', encoding='utf-8') as file:
                loaded_data_t = json.load(file)
            if log_file:
                with open(log_file, "r") as f:
                    loaded_log = f.readlines()
                r_ = GameRender(loaded_data_t["game"], loaded_data_t["winner"], loaded_log[1:])
            else:
                r_ = GameRender(loaded_data_t["game"], loaded_data_t["winner"])
            r_.run()

a = A()
a.run()