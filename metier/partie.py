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
    from metier.niveau import Niveau
    from metier.powerUp import PowerUp
    from config.config import Config
    from Entities.boutton import Button
    import copy
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class Partie(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.running = True
        self.draw()

    def draw(self):
        '''
        Cette classe gère le menu des niveaux et l'écran d'accueil.
        '''
        pygame.mixer.init()
        pygame.mixer.music.load("SONG/level.mp3")
        pygame.mixer.music.play(-1)

        # Crée les boutons une seule fois
        buttons = [
            Button(20, 30, "", "Unlocked", self.game.assets['level1']),
            Button(150, 50, "", "Locked", self.game.assets['level2']),
            Button(300, 25, "", "Locked", self.game.assets['level3']),
            Button(450, 250, "", "Locked", self.game.assets['level4']),
            Button(50, 350, "", "Locked", self.game.assets['level5']),
            Button(170, 370, "", "Locked", self.game.assets['level6']),
            Button(290, 400, "", "Locked", self.game.assets['level7']),
            Button(450, 400, "", "Locked", self.game.assets['level8']),
        ]
        button1 = buttons[0]  # bouton cliquable

        while self.running:
            self.game.display.blit(self.game.assets['background'][0], (0, 0))

            for button in buttons:
                button.draw(self.game)

            # 👉 On récupère tous les events une seule fois
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Clique sur le bouton 1
                if button1.handle_event(event):
                    while True:
                        level1 = Niveau(game=self.game, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")
                        self.game.currentLevel = level1
                        level1.run()

                        if level1.status == "menu":
                            self.reload()
                            break
                        elif level1.status == "restart":
                            self.reload()
                            continue
                        else:
                            break

            self.game.screen.blit(pygame.transform.scale(self.game.display, self.game.screen.get_size()), (0, 0))
            pygame.display.update()

        pygame.quit()
