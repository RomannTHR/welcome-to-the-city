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

class Niveau(pygame.sprite.Sprite):
    def __init__(self, player, plateformes,powersUp,ennemies, screen,state="locked"):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.plateformes = plateformes
        self.powersUp = powersUp
        self.ennemies = ennemies
        self.screen = screen
        self.state = state
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.plateformes)
        self.all_sprites.add(self.powersUp)
        self.all_sprites.add(self.ennemies)
        self.run(screen)

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

    def run(self,screen):
        clock = pygame.time.Clock()
        background = pygame.image.load("IMG/Level-Font/Free-City-Backgrounds-Pixel-Art2-1536x1024.jpg")  
        background = pygame.transform.scale(background, (Config.screen_width, Config.screen_height))  # Ajuster la taille si nécessaire
        running = True
        while running:
            clock.tick(60)  # Limite à 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.jump()
            # **1. Dessiner l'image de fond d'abord**
            screen.blit(background, (0, 0))
            
            # **2. Mettre à jour et dessiner les sprites**
            self.update()
            self.all_sprites.draw(self.screen)
            self.player.sended_projectile.draw(self.screen)

            # **3. Mettre à jour l'affichage (évite le clignotement)**
            pygame.display.update()  # Peut aussi être pygame.display.flip()
        pygame.quit()