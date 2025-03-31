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
    from Entities.boutton import Button
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class Partie(pygame.sprite.Sprite):
    def __init__(self, nom,niveaux,screen):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom
        self.niveaux = niveaux
        self.bouttons = []
        self.screen = screen
    def draw(self,screen):
        for i,niveau in enumerate(self.niveaux.sprites()):
            bouton = Button(Config.PARTIE_BOUTTON_X[i],Config.PARTIE_BOUTTON_Y[i],i,niveau.state,niveau.run,self.screen)
            self.bouttons.append(bouton)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in self.bouttons:
                    button.handle_event(event)
                for button in self.bouttons:
                    button.draw(screen)
            pygame.display.flip()

        pygame.quit()
