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
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(image_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.type = type


