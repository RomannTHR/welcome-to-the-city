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
    def __init__(self, game=False,player=False, plateformes=False,powersUp=False, steps=False, ennemies=False,cartes=False, screen=False, scroll=False, display=False, tilemap=False, state="Locked"):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.player = player
        self.plateformes = steps
        self.powersUp = powersUp
        self.ennemies = ennemies
        self.screen = screen
        self.display = display
        self.state = state
        self.scroll = scroll
        self.tilemap = tilemap
        self.cartes = cartes
        self.cartes_founded = 0
        self.all_sprites = pygame.sprite.Group()

        self.movement = [False, False]

        #self.all_sprites.add(self.player)
        self.all_sprites.add(self.plateformes)
        self.all_sprites.add(self.powersUp)
        self.all_sprites.add(self.ennemies)
        self.run()
        self.all_sprites.add(self.cartes)

    def update(self):
        pass
        #self.all_sprites.update()
        #self.all_sprites.update()
        #self.player.handle_collision(self.plateformes)
        #self.player.handle_collision_power(self.powersUp)
        #self.player.handle_collision_ennemie(self.ennemies)
        #for projectile in self.player.sended_projectile:
        #    projectile.handle_collision(self.ennemies)
        #self.player.sended_projectile.update()
        #self.all_sprites.update()
        #self.player.handle_collision(self.plateformes)
        #self.player.handle_collision_power(self.powersUp)
        #self.player.handle_collision_ennemie(self.ennemies)
        #self.cartes_founded += self.player.handle_collision_cartes(self.cartes)
        #for projectile in self.player.sended_projectile:
        #   projectile.handle_collision(self.ennemies)
        #self.player.sended_projectile.update()
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.player.sended_projectile.draw(self.screen)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.display.blit(self.game.assets['background'][0], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30

            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))
            
            self.game.clouds.update()
            self.game.clouds.render(self.display, offset=render_scroll)


            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.update_tiles()
            self.player.update(self.tilemap,(self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)


            font = pygame.font.SysFont("Arial", 16)
            self.display.blit(self.game.assets['items/cartes'][2], (0, 50))
            text = font.render(':' + str(self.player.map_number), True, (0, 0, 0))
            self.display.blit(text, (32, 50 + 32/4))
            #print(self.tilemap.physics_rect_around(self.player.pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True + self.player.playerSpeed
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True + self.player.playerSpeed
                    if event.key == pygame.K_SPACE and self.player.canDash and self.movement[0] > 0:
                            self.player.isDashingLeft = True
                    if event.key == pygame.K_SPACE and self.player.canDash and self.movement[1] > 0:
                            self.player.isDashingRight = True                  
                    if event.key == pygame.K_UP and self.player.isJumping == False:
                        self.player.velocity[1] = -3
                        self.player.isJumping = True
                    if event.key == pygame.K_UP and self.player.isWallJumping:
                        self.player.velocity[1] = -3.5
                        self.player.isWallJumping -= 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    

            self.update()
            
            #self.all_sprites.draw(self.display)
            

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            pygame.display.update()  
            clock.tick(60)  
        pygame.quit()