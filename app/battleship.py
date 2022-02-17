import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from game import Game
from scenes.settings import settings

def main():
    Game(pygame).on_init(settings).start()

if __name__ == '__main__':
    main()
