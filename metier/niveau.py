import sys
import random
import math
import os
import getopt
import pygame
from Entities.boutton import Button
from metier.entities import Enemy
from metier.powerUp import PowerUp
from metier.entities import Player

MAX_CARTES = 4
class Niveau(pygame.sprite.Sprite):
    def __init__(self, game,screen=False, scroll=False, display=False, tilemap=False, state="Locked"):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.player = Player(self.game,(100,100),(32,32))
        self.powersUp = []
        self.ennemies = []
        self.screen = screen
        self.display = display
        self.state = state
        self.isWin = False
        self.scroll = scroll
        self.tilemap = tilemap
        self.projectiles = []
        self.movement = [False, False]
        self.home_button = Button(550,30,"","Unlocked",self.game.assets['home_button'])
        self.button_back = Button(150, 250, "", "Unlocked", self.game.assets['back_button'])
        self.ennemies.append(Enemy(self.game,(215,300),(32,32),200,450))
        self.powersUp.append(PowerUp(100,125,"powerUp/coffre_ferme.png", "Jump"))
        self.jump_power_timer = None
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.player.sended_projectile.draw(self.screen)
        pygame.display.flip()
    def checkWin(self):
        if self.player.map_number >= MAX_CARTES:
            self.draw_win_screen()
            self.isWin = True
    def draw_win_screen(self):
        self.button_back.draw(self.game)
        self.display.blit(self.game.assets['win'][0], (-70, 0))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        status = "continue"
        while running:
            self.display.blit(self.game.assets['background'][0], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30

            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))
            
            self.game.clouds.update()
            self.game.clouds.render(self.display, offset=render_scroll)
            self.home_button.draw(self.game)

            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.update_tiles()
            self.player.update(self.tilemap,(self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            self.display.blit(self.game.assets['map_display'][0], (0,0))

            font = pygame.font.SysFont("Arial", 16)
            self.display.blit(self.game.assets['items/cartes'][2], (32, 32))
            text = font.render(': ' + str(self.player.map_number) + '/4', True, (0, 0, 0))
            self.display.blit(text, (64, 32 + 32/4))
            #print(self.tilemap.physics_rect_around(self.player.pos))
            for powerUp in self.powersUp:
                powerUp.update()
                powerUp.render(self.display,offset=render_scroll)
                if powerUp.rect.colliderect(self.player) and not powerUp.isFound:
                    powerUp.changeStateOpen()
                    powerUp.isFound = True
                    if powerUp.type == "Shield" and not self.player.isShielded:
                        self.player.life += 5
                    elif powerUp.type == "Jump":
                        self.player.jumpPower -= 2
                        self.jump_power_timer = pygame.time.get_ticks() + 10000

            for enemy in self.ennemies:
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
                for bullet in enemy.sended_Bullet:
                    bullet.update()
                    bullet.render(self.display, offset=render_scroll)
                    if bullet.rect().colliderect(self.player.rect()):
                        if self.player.explode():
                            status = "menu"
                    tilesAround = self.game.tilemap.physics_rect_around(bullet.pos)
                    for tile in tilesAround:
                        if bullet.rect().colliderect(tile[0]) or bullet.distance_traveled>=400:
                            if bullet in enemy.sended_Bullet:
                                enemy.sended_Bullet.remove(bullet)




            if not self.isWin:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        scale_x = self.display.get_width() / self.screen.get_width()
                        scale_y = self.display.get_height() / self.screen.get_height()
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mouse_scaled = (int(mouse_x * scale_x), int(mouse_y * scale_y))
                        scaled_event = pygame.event.Event(event.type, {"pos": mouse_scaled})

                        if self.home_button.handle_event(scaled_event) or self.button_back.handle_event(scaled_event):
                            status = "main"
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
                            if not self.player.is_attacking:
                                self.player.set_action('run')
                                self.player.is_attacking = True
                                self.player.attack_timer = int(0.5 * 60)
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
            if self.jump_power_timer is not None:
                if pygame.time.get_ticks() >= self.jump_power_timer:
                    self.player.jumpPower += 2
                    self.jump_power_timer =None

            self.checkWin()
            self.update()
            
            #self.all_sprites.draw(self.display)
            

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            pygame.display.update()  
            clock.tick(60)
        return status
