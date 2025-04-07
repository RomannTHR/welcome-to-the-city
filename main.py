import pygame
from pygame.locals import *
from metier.tilemap import Tilemap
from utils.utils import Animation, load_png, load_images, load_image
from metier.partie import Partie

from metier.entities import PhysicsEntities, Player,Enemy
from metier.clouds import Cloud, Clouds
from config.config import Config
from metier.niveau import Niveau

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Futur")

        self.screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.display = pygame.Surface((Config.env_width, Config.env_height))
        self.ennemies = []
        self.assets = {
            'background' : load_png('Background/4.png'),
            'cloud' : load_png('Background/cloud.png')[0],
            'grass' : load_images('Tiles/Grass'),
            'stone': load_images('Tiles/Stone'),
            'ice': load_images('Tiles/Ice'),
            'purplegrass': load_images('Tiles/PurpleGrass'),
            'decor' : load_images('Tiles/Decor'),
            'plateforme' : load_images('Tiles/Plateformes'),
            'player/idle' : Animation(load_images('Personnages/Idle'), img_dur=6),
            'player/run' : Animation(load_images('Personnages/Run'), img_dur=4),
            'player/jump' : Animation(load_images('Personnages/Idle'), img_dur=6),
            'enemy/idle' : Animation(load_images('Ennemies/Idle'), img_dur=15),
            'enemy/run' : Animation(load_images('Ennemies/Run'), img_dur=7),
            'level1': load_png('Buttons/level1.png'),
            'level2': load_png('Buttons/level2.png'),
            'level3': load_png('Buttons/level3.png'),
            'level4': load_png('Buttons/level4.png'),
            'level5': load_png('Buttons/level5.png'),
            'level6': load_png('Buttons/level6.png'),
            'level7': load_png('Buttons/level7.png'),
            'level8': load_png('Buttons/level8.png'),
            'bullet': load_png('Bullets/bullet.png')

        }

        self.clouds = Clouds(self.assets['cloud'], 8)

        self.player = Player(self,(100,50),(32,32))
        self.ennemies.append(Enemy(self,(215,300),(32,32),200,300))

        self.tilemap = Tilemap(self,tile_size=32)
        self.tilemap.load('Entities/save_editor/map.json')
        self.scroll = [0,0]
        level1 = Niveau(game=self, player=self.player, plateformes=False, powersUp=False, steps=False,
                        ennemies=self.ennemies, cartes=False, screen=self.screen, scroll=self.scroll,
                        display=self.display, tilemap=self.tilemap, state="Locked")

        self.currentLevel = level1
        self.initialPosition = [100,50]

    #Niveau 2 



    

    def run(self):

        #Start the level
        Partie(self)
        #Niveau(game=self,player=self.player,plateformes=False, powersUp=self.powersUp, steps=self.steps, ennemies=self.ennemies,cartes=False, screen=self.screen, scroll=self.scroll, display=self.display, tilemap=self.tilemap, state="Locked")


if __name__ == "__main__":
    Game().run()