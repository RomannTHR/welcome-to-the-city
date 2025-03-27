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
class Projectile(pygame.sprite.Sprite):

    def __init__(self,x,y,type,dammages=10):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("Projectiles/projectile.jpg")
        screen = pygame.display.get_surface()
        new_size = (120, 120)
        self.image = pygame.transform.scale(self.image, new_size)
        self.area = screen.get_rect()
        self.speed = 12
        self.x = x
        self.y = y
        self.type = type
        self.rect.x = self.x
        self.rect.y = self.y
        self.dammages = dammages
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()
        self.direction = 1
    def update (self):
        self.rect.x += self.speed * self.direction
    def explode(self):
        #Animation d'explosion
        self.kill()
    def handle_collision(self, ennemies):
        collisions = pygame.sprite.spritecollide(self, ennemies, False)
        if collisions:
            self.explode()
            collisions[0].hurt(self.dammages)