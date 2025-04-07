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


class Projectile:
    def __init__(self, x, y, direction=(1, 0), speed=1):
        self.image, _ = load_png("Bullets/bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.pos = [x, y]
        self.size = [20,20]
        self.direction = direction
        self.speed = speed

    def update(self):
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed
    def render(self, surface, offset=(0, 0)):
        surface.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[0])