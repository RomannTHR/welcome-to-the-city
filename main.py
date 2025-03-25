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
    from metier.powerUp import PowerUp
    from metier.ennemis import Ennemies
    from config.config import Config
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)
def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
    pygame.display.set_caption("Futur")
    powerUp1 = PowerUp(500,800,"powerUp/powerUp.png")
    powerUp2 = PowerUp(900, 800, "powerUp/powerUp.png")
    player1 = Player()
    step1 = Step(500, 550, "Objects/plateforme.jpg",False,0,750,"vert")
    ennemie1 = Ennemies(400,1200)
    steps = pygame.sprite.Group()
    powersUp = pygame.sprite.Group()
    ennemies = pygame.sprite.Group()
    powersUp.add(powerUp1,powerUp2)
    steps.add(step1)
    ennemies.add(ennemie1)
    Partie(player1, steps, powersUp,ennemies,screen)


if __name__ == "__main__":
    main()