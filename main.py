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
    from metier.niveau import Niveau
    from metier.platerforme import Step
    from metier.powerUp import PowerUp
    from metier.ennemis import Ennemies
    from metier.partie import Partie
    from config.config import Config
    from Ecran.start import Start
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)
def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
    pygame.display.set_caption("Welcome to the city")
    Start(screen)


if __name__ == "__main__":
    main()