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
    from config.config import Config
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class Partie(pygame.sprite.Sprite):
    def __init__(self, nom,niveaux):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom
        self.niveaux = niveaux
    def startNiveau(self, number_level_to_start):
        if(self.niveaux[number_level_to_start]).state=="unlocked":
            Level_to_start = self.niveaux[number_level_to_start]