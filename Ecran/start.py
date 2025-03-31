try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import pygame_gui
    from socket import *
    from pygame.locals import *
    from utils.utils import load_png,set_Rectangle
    from metier.personnage import Player
    from metier.niveau import Niveau
    from metier.platerforme import Step
    from metier.powerUp import PowerUp
    from metier.ennemis import Ennemies
    from metier.partie import Partie
    from metier.carte import Carte
    from config.config import Config
    from Entities.boutton import Button
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class Start(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.parties = pygame.sprite.Group()
        self.manager = pygame_gui.UIManager((Config.screen_width,Config.screen_height))
        self.input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350,275),(900,50)),manager=self.manager)
        self.clock = pygame.time.Clock()
        self._max_parties_number = 3
        self.button_ajouter = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 270), (100, 50)),
            text="Ajouter",
            manager=self.manager
        )
        self.boutons_start = []
        self.draw()
    def draw(self):
        while True:
            UI_REFRESH_RATE = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.button_ajouter:
                    nom =self.input.get_text()
                    if nom:
                        self.add_parties(nom)
                for bouton in self.boutons_start:
                    bouton.handle_event(event)
                for bouton in self.boutons_start:
                    bouton.draw(self.screen)
            for i,partie in enumerate(self.parties):
                set_Rectangle(500,350+(i*60),100,100,partie.nom,30,(50,150,255),(255, 255, 255),self.screen)
                bouton = Button(500,350+(i*60),partie.nom,"Unlocked",partie.draw,self.screen)
                self.boutons_start.append(bouton)
            self.manager.update(UI_REFRESH_RATE)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
    def add_parties(self,nom):

        #création des powersUp
        powerUp1 = PowerUp(500, 800, "powerUp/powerUp.jpg", "Life")
        powerUp2 = PowerUp(900, 800, "powerUp/powerUp.jpg", "Life")

        #création du joueur
        player1 = Player(0, 750)

        #création des plateformes
        step1 = Step(500, 550, "Objects/plateforme.jpg", 0, 750, "hor", 5)

        #création des ennemies
        ennemie1 = Ennemies(800, 750, 400, 1200)


        #création des cartes
        carte1 = Carte(500,800,"Cartes/carte.jpg",1)


        #création des sprite
        steps = pygame.sprite.Group()
        powersUp = pygame.sprite.Group()
        ennemies = pygame.sprite.Group()
        cartes = pygame.sprite.Group()
        #powersUp.add(powerUp1, powerUp2)
        steps.add(step1)
        #ennemies.add(ennemie1)
        cartes.add(carte1)
        niveau1 = Niveau(player1, steps, powersUp, ennemies,cartes, self.screen, "Unlocked")
        niveau2 = Niveau(player1, steps, powersUp, ennemies,cartes, self.screen)
        niveau3 = Niveau(player1, steps, powersUp, ennemies,cartes, self.screen)
        niveau4 = Niveau(player1, steps, powersUp, ennemies,cartes, self.screen)
        niveau5 = Niveau(player1, steps, powersUp, ennemies,cartes, self.screen)
        niveau6 = Niveau(player1, steps, powersUp, ennemies,cartes, self.screen)
        niveaux = pygame.sprite.Group()
        niveaux.add(niveau1, niveau2, niveau3, niveau4, niveau5, niveau6)
        partie = Partie(nom, niveaux, self.screen)
        self.parties.add(partie)
