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
    from metier.personnage import Player
    from metier.niveau import Niveau
    from metier.platerforme import Step
    from metier.powerUp import PowerUp
    from metier.ennemis import Ennemies
    from config.config import Config
    from Entities.boutton import Button
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        Niveau(game=self.game, player=self.game.player, plateformes=False, powersUp=self.game.powersUp, steps=self.game.steps,
                           ennemies=self.game.ennemies, cartes=False, screen=self.game.screen, scroll=self.game.scroll,
                           display=self.game.display, tilemap=self.game.tilemap, state="Locked")
            pygame.display.flip()

            buttons = []
            button1=Button(20,30,"caca","Unlocked",self.game.assets['level1'])
            button2=Button(150, 50,"caca","Locked",self.game.assets['level2'])
            button3=Button(300, 25,"caca","Locked",self.game.assets['level3'])
            button4=Button(450, 250,"caca","Locked",self.game.assets['level4'])
            button5=Button(50, 350,"caca","Locked",self.game.assets['level5'])
            button6=Button(170, 370,"caca","Locked",self.game.assets['level6'])
            button7=Button(290, 400,"caca","Locked",self.game.assets['level7'])
            button8=Button(450, 400,"caca","Locked",self.game.assets['level8'])
            buttons.extend([button1,button2,button3,button4,button5,button6,button7,button8])

            for button in buttons:
                button.draw(self.game)
            for event in pygame.event.get():
                #si boutton 1 est cliqué , on lance la partie1 ect...
                if button1.handle_event(event)==1:
                    level1 = Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")

                    self.game.currentLevel = level1
                    level1.run()
                if button2.handle_event(event) == 1 and button2.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game, player=self.game.player, plateformes=False, powersUp=False,
                           steps=False, ennemies=self.game.ennemies, cartes=False, screen=self.game.screen,
                           scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap,
                           state="Locked")
                if button3.handle_event(event)==1 and button3.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")

                if button4.handle_event(event)==1 and button4.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")

                if button5.handle_event(event)==1 and button5.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")
                if button6.handle_event(event)==1 and button6.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")
                if button7.handle_event(event)==1 and button7.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")
                if button8.handle_event(event)==1 and button8.state != "Locked":
                    self.game.currentLevel =Niveau(game=self.game,player=self.game.player,plateformes=False, powersUp=False, steps=False, ennemies=self.game.ennemies,cartes=False, screen=self.game.screen, scroll=self.game.scroll, display=self.game.display, tilemap=self.game.tilemap, state="Locked")


            self.game.screen.blit(pygame.transform.scale(self.game.display, self.game.screen.get_size()), (0, 0))

            pygame.display.update()

        pygame.quit()
