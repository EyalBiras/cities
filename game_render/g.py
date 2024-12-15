import gzip
import json

import pygame
from r import GameRender
from menu import Menu



class A:
    def __init__(self):
        pygame.init()

    def run(self):
        m = Menu()
        f = m.run()
        with gzip.open(f, 'rt', encoding='utf-8') as file:
            loaded_data_t = json.load(file)
        r_ = GameRender(loaded_data_t)
        r_.run()

a = A()
a.run()