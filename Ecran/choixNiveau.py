try:
    import sys
    import random
    import math
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bouton cliquable")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
button_rect = pygame.Rect(300, 250, 200, 80)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Bouton cliqué !")

    pygame.draw.rect(screen, GREEN, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Clique-moi", True, RED)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
