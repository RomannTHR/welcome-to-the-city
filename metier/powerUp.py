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
class PowerUp(pygame.sprite.Sprite):

    def __init__(self,x,y,image_path,type):
        self.image, self.rect = load_png(image_path)
        self.anim_offset = (-3, -3)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.type = type
        self.isOpen = False
        self.isFound = False

    def changeStateOpen(self):
        self.isOpen = not self.isOpen
    def update(self):
        if self.isOpen:
            self.image, _ = load_png("powerUp/coffre_ouvert.png")
        else:
            self.image,_ = load_png("powerUp/coffre_ferme.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
    def render(self,surface,offset=(0,0)):
        surface.blit(self.image, (self.x - offset[0] + self.anim_offset[0], self.y - offset[1] + self.anim_offset[1]))
