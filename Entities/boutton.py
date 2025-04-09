import pygame

class Button:
    '''
    Cette classe représente les bouttons sur le jeux pour une manipulation plus facile de ceux-ci
    '''
    def __init__(self,x,y,text,state,img):
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y
        self.text = text
        self.state = state
        self.img = img
    def render(self,surf):
        if self.state=="Locked":
            self.img[0].set_alpha(100)
        surf.blit(self.img[0], ((self.x,self.y)))
    def draw(self,game):
        mouse_pos = pygame.mouse.get_pos()
        self.render(game.display)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and (self.state =="Unlocked" or self.state=="Start"):
            if self.rect.collidepoint(event.pos):
                sound = pygame.mixer.Sound("SONG/button_click.mp3")
                sound.play()
                return True
        return False
