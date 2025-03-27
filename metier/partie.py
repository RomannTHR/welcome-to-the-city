import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame import *
from utils.utils import load_png
from metier.personnage import Player
from metier.platerforme import Step
from config.config import Config
from metier.projectiles import Projectile

class Partie(pygame.sprite.Sprite):
    def __init__(self, player, plateformes,powersUp,ennemies, screen):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.plateformes = plateformes
        self.powersUp = powersUp
        self.ennemies = ennemies
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.plateformes)

        #Charger le background de la partie 

        self.background = pygame.image.load(os.path.join("IMG/Level-Font", "Free-City-Backgrounds-Pixel-Art2-1536x1024.jpg")).convert()
        self.bg_width = self.background.get_width()


        self.all_sprites.add(self.powersUp)
        self.all_sprites.add(self.ennemies)
        self.run()

    def update(self):
        self.all_sprites.update()
        self.all_sprites.update()
        self.player.handle_collision(self.plateformes)
        self.player.handle_collision_power(self.powersUp)
        self.player.handle_collision_ennemie(self.ennemies)
        for projectile in self.player.sended_projectile:
            projectile.handle_collision(self.ennemies)
        self.player.sended_projectile.update()
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.player.sended_projectile.draw(self.screen)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.jump()
            self.update()
            self.draw()
            clock.tick(60)
        pygame.quit()