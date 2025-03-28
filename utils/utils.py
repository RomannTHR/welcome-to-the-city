try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join("IMG/", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()
def set_Rectangle(x,y,width,height,text,font_size,background_color,font_color,screen):
    font = pygame.font.Font(None, font_size)

    text_surface = font.render(text,True,font_color)
    square_rect = pygame.Rect(x,y,width,height)
    pygame.draw.rect(screen, background_color, square_rect)
    text_rect = text_surface.get_rect(center=square_rect.center)
    screen.blit(text_surface, text_rect)