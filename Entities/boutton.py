import pygame
from utils.utils import  load_png

class Button:
    def __init__(self,x,y,text,state,action=None):
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.action = action
        self.text = text
        self.state = state

    def draw(self,screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
