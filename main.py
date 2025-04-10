import pygame
from pygame.locals import *
from metier.tilemap import Tilemap
from utils.utils import Animation, load_png, load_images, load_image
from metier.partie import Partie

from metier.entities import FinalBoss, PhysicsEntities, Player,Enemy
from metier.clouds import Cloud, Clouds
from config.config import Config
from metier.niveau import Niveau
from metier.powerUp import PowerUp

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Futur")

        self.screen = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.display = pygame.Surface((Config.env_width, Config.env_height))
        self.assets = {
            'background' : load_png('Background/4.png'),
            'cloud' : load_png('Background/cloud.png')[0],
            'map_display' : load_png('Items/Cartes/scrolled_map.png'),
            'monster_display' : load_png('Others/monster.png'),
            'grass' : load_images('Tiles/Grass'),
            'stone': load_images('Tiles/Stone'),
            'ice': load_images('Tiles/Ice'),
            'purplegrass': load_images('Tiles/PurpleGrass'),
            'decor' : load_images('Tiles/Decor'),
            'plateforme' : load_images('Tiles/Plateformes'),
            'jumper' : load_images('Tiles/Jumper'),
            'items/cartes' : load_images('Items/Cartes'),
            'nocollisions': load_images('Tiles/NoCollisions'),
            'player/idle' : Animation(load_images('Personnages/Idle'), img_dur=6),
            'player/run' : Animation(load_images('Personnages/Run'), img_dur=4),
            'player/jump' : Animation(load_images('Personnages/Idle'), img_dur=6),
            'player/attack' : Animation(load_images('Personnages/Attack'), img_dur=6),
            'enemy/idle' : Animation(load_images('Ennemies/Idle'), img_dur=15),
            'enemy/idle' : Animation(load_images('Ennemies/Walk'), img_dur=10),
            'enemy/run' : Animation(load_images('Ennemies/Run'), img_dur=7),
            'finalboss/idle' : Animation(load_images('FinalBoss/Idle'), img_dur=8),
            'finalboss/attack' : Animation(load_images('FinalBoss/Attack'), img_dur=12),
            'finalboss/death' : Animation(load_images('FinalBoss/Death'), img_dur=20),
            'finalboss/spawning' : Animation(load_images('FinalBoss/Spawning'), img_dur=6),
            'level1': load_png('Buttons/level1.png'),
            'level2': load_png('Buttons/level2.png'),
            'level3': load_png('Buttons/level3.png'),
            'level4': load_png('Buttons/level4.png'),
            'level5': load_png('Buttons/level5.png'),
            'level6': load_png('Buttons/level6.png'),
            'level7': load_png('Buttons/level7.png'),
            'level8': load_png('Buttons/level8.png'),
            'home_button': load_png('Buttons/home.png'),
            'back_button': load_png('Buttons/back.png'),
            'win': load_png('Background/win.png'),
            'bullet': load_png('Bullets/bullet.png')
        }
        self.ennemies = []
        self.powersUp = []
        self.clouds = Clouds(self.assets['cloud'], 8)

        self.player = Player(self,(100,100),(32,32))
        self.ennemies.append(Enemy(self,(215,300),(32,32),200,450))
        self.powersUp.append(PowerUp(100,125,"powerUp/coffre_ferme.png", "Jump"))
        self.tilemap = Tilemap(self,tile_size=32)
        self.finalboss = FinalBoss(self, (-608,-800), (100,100))
        self.tilemap.load('Entities/save_editor/map.json')
        self.scroll = [0,0]
        self.initialPosition = [100,50]

    #Niveau 2 



    def run(self):

        #Start the level
        Partie(self)
        #Niveau(game=self,player=self.player,plateformes=False, powersUp=self.powersUp, steps=self.steps, ennemies=self.ennemies,cartes=False, screen=self.screen, scroll=self.scroll, display=self.display, tilemap=self.tilemap, state="Locked")


if __name__ == "__main__":
    Game().run()