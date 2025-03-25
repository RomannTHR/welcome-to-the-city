try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
    from utils.utils import load_png
    from metier.personnage import Player
    from metier.partie import Partie
    from metier.platerforme import Step
    from config.config import Config
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)
def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
    pygame.display.set_caption("Futur")

    player1 = Player()
    step1 = Step(500, 550, "Objects/plateforme.jpg",False,0,750,"vert")
    steps = pygame.sprite.Group()
    steps.add(step1)
    Partie(player1, steps, screen)


if __name__ == "__main__":
    main()