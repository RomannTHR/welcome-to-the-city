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


class Partie(pygame.sprite.Sprite):
    def __init__(self, player, plateformes, screen):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.plateformes = plateformes
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.plateformes)
        self.run()

    def update(self):
        self.all_sprites.update()
        self.player.handle_collision(self.plateformes)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Remplit l'écran en noir
        self.all_sprites.draw(self.screen)
        pygame.display.flip()  # Met à jour l'affichage

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