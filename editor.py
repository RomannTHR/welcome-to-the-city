import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame.locals import *
from metier.tilemap import Tilemap
from utils.utils import load_images
#from metier.personnage import Player
from metier.niveau import Niveau
from metier.entities import PhysicsEntities

from config.config import Config

RENDER_SCALE = 2
CAMERA_SPEED = 2

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Futur")

        self.screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.display = pygame.Surface((Config.env_width, Config.env_height))
        
        

        self.assets = {
            'grass' : load_images('Titles/Grass'),
            'stone': load_images('Titles/Stone'),
            'ice': load_images('Titles/Ice'),
            'purplegrass': load_images('Titles/PurpleGrass'),
            'decor' : load_images('Titles/Decor'),
            'platerforme' : load_images('Titles/Plateformes')
        }

        print(self.assets['grass'])

        self.tilemap = Tilemap(self,tile_size=32)

        self.scroll = [0,0]

        self.tile_list = list(self.assets)
        self.current_tile_group = 0
        self.current_tile_variant = 0

        self.movement = [False, False, False, False]
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
    #Niveau 2 



    

    def run(self):

        clock = pygame.time.Clock()
        running = True
        while running:
            #self.display.blit(self.assets['background'][0], (0,0))
            self.display.fill((0,0,0))
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * CAMERA_SPEED
            self.scroll[1] += (self.movement[2] - self.movement[3]) * CAMERA_SPEED
            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))

            current_tile_img = self.assets[self.tile_list[self.current_tile_group]][self.current_tile_variant].copy()
            current_tile_img.set_alpha(100)
            self.tilemap.render(self.display, offset=render_scroll)
            self.display.blit(current_tile_img, (5,5))


            mouse_position = pygame.mouse.get_pos()

            mouse_position = (mouse_position[0] / RENDER_SCALE, mouse_position[1] / RENDER_SCALE)
            tile_pos = (int(mouse_position[0] + self.scroll[0]) // self.tilemap.tile_size, int(mouse_position[1] + self.scroll[1]) // self.tilemap.tile_size)

            if self.ongrid: 
                self.display.blit(current_tile_img, (int(tile_pos[0] * self.tilemap.tile_size - self.scroll[0]) ,int(tile_pos[1] * self.tilemap.tile_size - self.scroll[1])))
            else:
                self.display.blit(current_tile_img, (int(mouse_position[0]  - self.scroll[0]) ,int(mouse_position[1] - self.scroll[1])))

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] =  {'type': self.tile_list[self.current_tile_group], 'variant': self.current_tile_variant, 'pos': (tile_pos[0], tile_pos[1])}

            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del(self.tilemap.tilemap[tile_loc]) 
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(mouse_position):
                        self.tilemap.offgrid_tiles.remove(tile)
            
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.current_tile_group], 'variant': self.current_tile_variant, 'pos': (mouse_position[0] + self.scroll[0], mouse_position[1] + self.scroll[0])})
                    if event.button == 3:
                        self.right_clicking = True                            
                    if self.shift == True:
                        if event.button == 4:
                            self.current_tile_variant = (self.current_tile_variant + 1) % len(self.assets[self.tile_list[self.current_tile_group]])
                        if event.button == 5:
                            self.current_tile_variant = (self.current_tile_variant - 1) % len(self.assets[self.tile_list[self.current_tile_group]])
                    else:
                        if event.button == 4:
                            self.current_tile_group = (self.current_tile_group + 1) % len(self.tile_list)
                        if event.button == 5:
                            self.current_tile_group = (self.current_tile_group - 1) % len(self.tile_list)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[3] = True
                    if event.key == pygame.K_DOWN :
                        self.movement[2] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('Entities/save_editor/map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.current_tile_variant = 0
                        self.shift = not self.shift 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[3] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[2] = False
                    
                    

                   

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            pygame.display.update()  
            clock.tick(60)  
        pygame.quit()

if __name__ == "__main__":
    Game().run()