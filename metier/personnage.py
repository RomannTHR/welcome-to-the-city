try:
    import time
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
class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("Personnages/Idle/000.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 5
        self.life = 10
        self.is_jumping = False
        self.y_velocity = 0
        self.reinit()
        self.rect.x = x
        self.rect.y = y
        self.last_shot_time = 0
        self.shoot_cooldown = 0.5
        self.last_ennemy_time = 0
        self.last_ennemy_cooldown = 2
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()
        self.sended_projectile = pygame.sprite.Group()
        self.power = "None"
        self.isShielded = False

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
            self.tirer()
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
            self.y_velocity = -15
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
        if self.on_ground:
            self.rect.x += collisions[0].velocity*2
    def handle_collision_cartes(self, cartes):
        collisions = pygame.sprite.spritecollide(self, cartes, False)
        for carte in collisions:
            carte.kill()
            return 1
        return 0

    def handle_collision_power(self, powersUp):
        collisions = pygame.sprite.spritecollide(self, powersUp, False)
        if collisions :
            if collisions[0].type == "Projectile":
                self.power = "Tirer"
            elif collisions[0].type == "Life":
                if self.isShielded == False:
                    self.isShielded = True
                    self.image = pygame.transform.rotozoom(self.image, 0, 1.5)
                    self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

            collisions[0].kill()
    def handle_collision_ennemie(self, ennemies):
        collisions = pygame.sprite.spritecollide(self, ennemies, False)

        if collisions :
            #Si le joueur arrive du haut et qu'il est en train de redescendre
            if self.y_velocity > 0:
                collisions[0].hurt(10)
            else:
                current_time = time.time()
                if current_time - self.last_ennemy_time > self.last_ennemy_cooldown:
                    self.hurt(collisions[0].dammages)
                    self.last_ennemy_time = current_time
