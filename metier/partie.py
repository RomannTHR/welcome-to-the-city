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
        while self.running:
            self.game.display.blit(self.game.assets['background'][0], (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()

            buttons = []
            button1=Button(20,30,"","Unlocked",self.game.assets['level1'])
            button2=Button(150, 50,"","Locked",self.game.assets['level2'])
            button3=Button(300, 25,"","Locked",self.game.assets['level3'])
            button4=Button(450, 250,"","Locked",self.game.assets['level4'])
            button5=Button(50, 350,"","Locked",self.game.assets['level5'])
            button6=Button(170, 370,"","Locked",self.game.assets['level6'])
            button7=Button(290, 400,"","Locked",self.game.assets['level7'])
            button8=Button(450, 400,"","Locked",self.game.assets['level8'])
            buttons.extend([button1,button2,button3,button4,button5,button6,button7,button8])

            for button in buttons:
                button.draw(self.game)
            for event in pygame.event.get():
                #si boutton 1 est cliqué , on lance la partie1 ect...
                if button1.handle_event(event)==1:
                    while True:
                        level1 = Niveau(game=self.game, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")
                        self.game.currentLevel = level1
                        game_state = level1.run()
                        if game_state == "menu":
                            self.reload()
                            break
                        elif game_state == "restart":
                            self.reload()
                            continue
                        else:
                            break

            self.game.screen.blit(pygame.transform.scale(self.game.display, self.game.screen.get_size()), (0, 0))

            pygame.display.update()

        pygame.quit()
