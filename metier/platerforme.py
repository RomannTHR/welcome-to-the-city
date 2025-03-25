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
class Step(pygame.sprite.Sprite):

    def __init__(self,x,y,image_path,movable,start,end,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = 1
        self.movable = movable
        self.start = start
        self.end = end
        self.movment_direction = direction
    def update(self):
        if self.movable:
            if self.movment_direction == "hor":
                self.rect.x += self.speed * self.direction

                if self.rect.x >= self.end:
                    self.direction = -1
                elif self.rect.x <= self.start:
                    self.direction = 1
            elif self.movment_direction == "vert":
                self.rect.y += self.speed * self.direction

                if self.rect.y >= self.end:
                    self.direction = -1
                elif self.rect.y <= self.start:
                    self.direction = 1
