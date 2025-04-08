import sys
import random
import math
import os
import getopt
import pygame
from Entities.boutton import Button


class Niveau(pygame.sprite.Sprite):
    def __init__(self, game=False,player=False, plateformes=False,powersUp=False, steps=False, ennemies=False,cartes=False, screen=False, scroll=False, display=False, tilemap=False, state="Locked"):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.player = player
        self.plateformes = steps
        self.powersUp = powersUp
        self.ennemies = ennemies
        self.screen = screen
        self.display = display
        self.state = state
        self.scroll = scroll
        self.tilemap = tilemap
        self.cartes = cartes
        self.cartes_founded = 0
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = []
        self.movement = [False, False]
        self.home_button = Button(20,30,"","Unlocked",self.game.assets['home_button'])
        #self.all_sprites.add(self.player)

    def update(self):
        pass
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.player.sended_projectile.draw(self.screen)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.display.blit(self.game.assets['background'][0], (0,0))
            self.home_button.draw(self.game)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30

            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))
            
            self.game.clouds.update()
            self.game.clouds.render(self.display, offset=render_scroll)


            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.update_tiles()
            self.player.update(self.tilemap,(self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)


            font = pygame.font.SysFont("Arial", 16)
            self.display.blit(self.game.assets['items/cartes'][2], (0, 50))
            text = font.render(':' + str(self.player.map_number), True, (0, 0, 0))
            self.display.blit(text, (32, 50 + 32/4))
            
            #print(self.tilemap.physics_rect_around(self.player.pos))
            for powerUp in self.game.powerUp:
                powerUp.update()
                powerUp.render(self.display,offset=render_scroll)
                if powerUp.rect.colliderect(self.player) and not powerUp.isFound:
                    powerUp.changeStateOpen()
                    powerUp.isFound = True
                    if powerUp.type ==  "Shield" and not self.player.isShielded:
                        self.player.life += 5
                    elif powerUp.type == "Jump" :
                        self.player.jumpPower -=2
            for enemy in self.game.ennemies:
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
                for bullet in enemy.sended_Bullet:
                    bullet.update()
                    bullet.render(self.display, offset=render_scroll)
                    if bullet.rect().colliderect(self.player.rect()):
                        self.player.hurt(enemy.dammages)
                    tilesAround = self.game.tilemap.physics_rect_around(bullet.pos)
                    for tile in tilesAround:
                        if bullet.rect().colliderect(tile[0]):
                            if bullet in enemy.sended_Bullet:
                                enemy.sended_Bullet.remove(bullet)






            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.home_button.handle_event(event):
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True + self.player.playerSpeed
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True + self.player.playerSpeed
                    if event.key == pygame.K_SPACE and self.player.canDash and self.movement[0] > 0:
                            self.player.isDashingLeft = True
                    if event.key == pygame.K_SPACE and self.player.canDash and self.movement[1] > 0:
                            self.player.isDashingRight = True                  
                    if event.key == pygame.K_UP and self.player.isJumping == False:
                        self.player.velocity[1] = self.player.jumpPower
                        self.player.isJumping = True
                    if event.key == pygame.K_UP and self.player.isWallJumping:
                        self.player.velocity[1] = self.player.jumpPower
                        self.player.isWallJumping -= 1
                    if event.key == pygame.K_g:
                        self.player.set_action('run')
                        for enemy in self.ennemies:
                            distance_x = abs(self.player.pos[0] - enemy.pos[0])
                            distance_y = abs(self.player.pos[1] - enemy.pos[1])
                            if distance_x < 30 and distance_y < 10:
                                enemy.hurt(self.player.dammages)
                                self.ennemies.remove(enemy)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    

            self.update()
            
            #self.all_sprites.draw(self.display)
            

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            pygame.display.update()  
            clock.tick(60)