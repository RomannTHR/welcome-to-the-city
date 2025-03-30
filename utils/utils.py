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

BASE_IMG_PATH = 'IMG/'


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

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(os.path.join("IMG/", path))):
        images.append(load_image(path + '/' + img_name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images,self.img_duration,self.loop)

    def update(self):
        if self.loop: #If the animation need to restart permanantly
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) # The modulo here is usefull to make a loop to a maximum value (here : self.img_duration * len(self.images) which is all the frames that is gonna be generated)
        else:
            self.frame = min(self.frame+1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
                
    def img(self):
        return self.images[int(self.frame / self.img_duration)] #the frame is the frame of the game and not of the image, that means to get the correct image we have to divide by his duration time
