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
    from config.config import Config
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)
class Ennemies(pygame.sprite.Sprite):

    def __init__(self, x,y,start,end,life=10,dammages=10):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("Personnages/Idle/000.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 2
        self.life = life
        self.dammages = dammages
        self.start = start
        self.end = end
        self.rect.x = x
        self.rect.y = y
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()
        self.direction = 1
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x >= self.end:
            self.direction = -1
        elif self.rect.x <= self.start:
            self.direction = 1

    def explode(self):
        #Annimation de mort
        self.kill()

    def hurt(self, dammages):
        if self.life>dammages:
            self.life -= dammages
        else :
            self.explode()