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
    pygame.display.set_caption("Futur")
    powerUp1 = PowerUp(500,800,"powerUp/powerUp.jpg","Life")
    powerUp2 = PowerUp(900, 800, "powerUp/powerUp.jpg","Life")
    player1 = Player(0,750)
    step1 = Step(500, 550, "Objects/plateforme.jpg",0,750,"hor",5)
    ennemie1 = Ennemies(800,750,400,1200)
    steps = pygame.sprite.Group()
    powersUp = pygame.sprite.Group()
    ennemies = pygame.sprite.Group()
    powersUp.add(powerUp1,powerUp2)
    steps.add(step1)
    ennemies.add(ennemie1)
    niveau1 = Niveau(player1, steps, powersUp,ennemies,screen,"Unlocked")
    niveau2 = Niveau(player1, steps, powersUp,ennemies,screen)
    niveau3 = Niveau(player1, steps, powersUp,ennemies,screen)
    niveau4 = Niveau(player1, steps, powersUp,ennemies,screen)
    niveau5 = Niveau(player1, steps, powersUp,ennemies,screen)
    niveau6 = Niveau(player1, steps, powersUp,ennemies,screen)
    niveaux = pygame.sprite.Group()
    niveaux.add(niveau1,niveau2,niveau3,niveau4,niveau5,niveau6)
    #Partie("Test", niveaux,screen)
    Start(screen)


if __name__ == "__main__":
    main()