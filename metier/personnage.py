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
    from metier.projectiles import Projectile
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("Personnages/ssm.jpg")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.life = 10
        self.is_jumping = False
        self.y_velocity = 0
        self.reinit()
        self.rect.x = 0
        self.rect.y = 700
        self.sended_projectile = pygame.sprite.Group()

    def reinit(self):
        self.movepos = [0,0]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.movepos = [0, self.speed]
        elif keys[pygame.K_LEFT]:
            self.movepos = [-self.speed, 0]
        elif keys[pygame.K_RIGHT]:
            self.movepos = [self.speed, 0]
        elif keys[pygame.K_SPACE]:
            projectile = Projectile(self.rect.x, self.rect.y, "Rien")
            self.sended_projectile.add(projectile)
        else:
            self.movepos = [0, 0]
        self.rect.x += self.movepos[0]
        self.rect.y += self.movepos[1]
        self.rect.x = max(0, min(self.rect.x, Config.env_width))
        self.rect.y = max(0, min(self.rect.y, Config.env_height))
        self.y_velocity += Config.GRAVITY
        self.sended_projectile.update()
        self.rect.y += self.y_velocity
        if self.rect.bottom >= Config.env_height:
            self.rect.bottom = Config.env_height
            self.y_velocity = 0
            self.is_jumping = False
            self.on_ground = True
    def jump(self):
        if not self.is_jumping or self.on_ground:
            self.y_velocity = -20
            self.is_jumping = True

    def handle_collision(self, plateformes):
        self.on_ground = False
        collisions = pygame.sprite.spritecollide(self, plateformes, False)
        for plateforme in collisions:
            if self.y_velocity > 0:
                self.rect.bottom = plateforme.rect.top
                self.y_velocity = 0
                self.on_ground = True
                break
            elif self.y_velocity < 0:
                self.rect.top = plateforme.rect.bottom
                self.y_velocity = 0

    def handle_collision_power(self, powersUp):
        collisions = pygame.sprite.spritecollide(self, powersUp, False)
        if collisions :
                collisions[0].kill()
    def handle_collision_ennemie(self, ennemies):
        collisions = pygame.sprite.spritecollide(self, ennemies, False)
        if collisions :
            print("aille")