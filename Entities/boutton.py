import pygame

class Button:
    def __init__(self,x,y,text,state,action,parameter):
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.action = action
        self.text = text
        self.state = state
        self.parameter = parameter

    def draw(self,screen):
        if(self.state =="Locked"):
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        elif(self.state=="Unlocked"):
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
        elif(self.state=="Start"):
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and (self.state =="Unlocked" or self.state=="Start"):
            print("iii")
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action(self.parameter)
