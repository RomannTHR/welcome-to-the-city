import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame.locals import *
from metier.tilemap import Tilemap
from utils.utils import Animation, load_png, load_images, load_image
#from metier.personnage import Player
from metier.partie import Partie
from metier.niveau import Niveau
from metier.platerforme import Step
from metier.powerUp import PowerUp
from metier.ennemis import Ennemies
from metier.entities import PhysicsEntities, Player
from metier.clouds import Cloud, Clouds
from Entities.boutton import Button
from config.config import Config


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Futur")

        self.screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.display = pygame.Surface((Config.env_width, Config.env_height))
        
        

        self.assets = {
            'background' : load_png('Background/4.png'),
            'cloud' : load_png('Background/cloud.png')[0],
            'grass' : load_images('Titles/Grass'),
            'stone': load_images('Titles/Stone'),
            'ice': load_images('Titles/Ice'),
            'purplegrass': load_images('Titles/PurpleGrass'),
            'decor' : load_images('Titles/Decor'),
            'player/idle' : Animation(load_images('Personnages/Idle'), img_dur=6),
            'player/run' : Animation(load_images('Personnages/Run'), img_dur=4),
            'player/jump' : Animation(load_images('Personnages/Idle'), img_dur=6),
            'level1': load_png('Buttons/level1.png'),
            'level2': load_png('Buttons/level2.png'),
            'level3': load_png('Buttons/level3.png'),
            'level4': load_png('Buttons/level4.png'),
            'level5': load_png('Buttons/level5.png'),
            'level6': load_png('Buttons/level6.png'),
            'level7': load_png('Buttons/level7.png'),
            'level8': load_png('Buttons/level8.png')
        }

        self.clouds = Clouds(self.assets['cloud'], 8)

        button1 = Button(50,50,"Test","Unlocked",self.assets['level1'])

        self.player = Player(self,(100,50),(32,32))

        self.buttons = [button1]

        self.tilemap = Tilemap(self,tile_size=32)

        self.scroll = [0,0]

        powerUp1 = PowerUp(500,800,"powerUp/powerUp.jpg","Life")
        powerUp2 = PowerUp(900, 800, "powerUp/powerUp.jpg","Life")
        step1 = Step(500, 550, "Objects/plateforme.jpg",0,750,"hor",5)
        ennemie1 = Ennemies(800,750,400,1200)

        self.steps = pygame.sprite.Group()
        self.powersUp = pygame.sprite.Group()
        self.ennemies = pygame.sprite.Group()

        self.powersUp.add(powerUp1,powerUp2)
        self.steps.add(step1)
        self.ennemies.add(ennemie1)


    #Niveau 2 



    

    def run(self):

        #Start the level
        Partie(self)
        #Niveau(game=self,player=self.player,plateformes=False, powersUp=self.powersUp, steps=self.steps, ennemies=self.ennemies,cartes=False, screen=self.screen, scroll=self.scroll, display=self.display, tilemap=self.tilemap, state="Locked")


if __name__ == "__main__":
    Game().run()