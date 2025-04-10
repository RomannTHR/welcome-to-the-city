import sys
import pygame
from Entities.boutton import Button
from metier.entities import Enemy
from metier.powerUp import PowerUp
from metier.entities import Player

MAX_CARTES = 4
class Niveau(pygame.sprite.Sprite):
    '''
    Cette classe représente un niveau
    Celle-ci gère les entrées du clavier, les interactions entre le personnage , les blocs de décors ,les ennemies et les powers-up
    '''
    def __init__(self, game,screen=False, scroll=False, display=False, tilemap=False, state="Locked"):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.player = Player(self.game,(100,100),(32,32))
        self.powersUp = []
        self.ennemies = []
        self.finalboss = self.game.finalboss
        self.screen = screen
        self.display = display
        self.state = state
        self.isWin = False
        self.scroll = scroll
        #la map de base
        self.tilemap = tilemap
        self.finalboss_number = 0
        self.cartes_founded = 0
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = []
        self.movement = [False, False]
        #représente le bouton de retour au menu visible tout le temps en haut à droite
        self.home_button = Button(450,30,"","Unlocked",self.game.assets['home_button'])
        #représente le bouton de retour au menu, visible lorsque l'on a gagné le niveau
        self.button_back = Button(150, 250, "", "Unlocked", self.game.assets['back_button'])
        #crée les instances de classe des enemies
        self.ennemies.append(Enemy(self.game,(215,300),(32,32),200,450))
        #crée les instances de classe des powers-up
        self.powersUp.append(PowerUp(100,125,"powerUp/coffre_ferme.png", "Jump"))
        self.jump_power_timer = None
        #Représente l'état du jeux pour une mise en pause ou un reload
        self.status= None

        self.running = True
    #regarde si le joueur a trouvé toute les cartes
    def checkWin(self):
        if self.player.map_number >= MAX_CARTES:
            self.draw_win_screen()
            self.isWin = True
    def draw_win_screen(self):
        self.button_back.draw(self.game)
        self.display.blit(self.game.assets['win'][0], (-70, 0))

    def run(self):
        clock = pygame.time.Clock()
        status = "continue"
        while self.running:
            self.display.blit(self.game.assets['background'][0], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30

            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))
            
            self.game.clouds.update()
            self.game.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.update_tiles()
            self.player.update(self.tilemap,(self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)


            self.handle_powersUp()
            self.handle_ennemies()
            self.display.blit(self.game.assets['map_display'][0], (0, 0))

            
            if self.finalboss != None:
                self.finalboss.render(self.display, offset=render_scroll)
                self.finalboss.update(self.tilemap, self.player)
                if self.finalboss.is_dead:
                    self.finalboss_number = 1
                    self.finalboss = None
            
            font = pygame.font.SysFont("Arial", 16)
            self.display.blit(self.game.assets['items/cartes'][2], (32, 32))
            text = font.render(': ' + str(self.player.map_number) + '/4', True, (0, 0, 0))
            self.display.blit(text, (64, 32 + 32/4))

            self.display.blit(self.game.assets['monster_display'][0], (32, 64))
            text = font.render(': ' + str(self.finalboss_number) + '/1', True, (0, 0, 0))
            self.display.blit(text, (64, 64 + 32/4))

            self.home_button.draw(self.game)
            if not self.isWin:
                self.handle_pygame_events()
            if self.jump_power_timer is not None:
                if pygame.time.get_ticks() >= self.jump_power_timer:
                    self.player.jumpPower += 2
                    self.jump_power_timer =None
            self.checkWin()
            self.update()
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            pygame.display.update()  
            clock.tick(60)
        return status
    #gère les powers-up (affichage, collision,effet sur le joueur)
    def handle_powersUp(self):
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        for powerUp in self.powersUp:
            powerUp.update()
            powerUp.render(self.display, offset=render_scroll)
            if powerUp.rect.colliderect(self.player) and not powerUp.isFound:
                powerUp.changeStateOpen()
                sound = pygame.mixer.Sound("SONG/powerUp.mp3")
                sound.play()
                powerUp.isFound = True
                if powerUp.type == "Shield" and not self.player.isShielded:
                    self.player.life += 5
                elif powerUp.type == "Jump":
                    self.player.jumpPower -= 2
                    self.jump_power_timer = pygame.time.get_ticks() + 10000
    #gère les ennemies(affichage, collisions avec les murs, mort)
    def handle_ennemies(self):
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        for enemy in self.ennemies:
            enemy.update(self.tilemap)
            enemy.render(self.display, offset=render_scroll)
            self.handle_bullets(enemy)
    #gère les balles (affichage, collisions avec le joueur et les murs, explosion)
    def handle_bullets(self,enemy):
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        for bullet in enemy.sended_Bullet:
            bullet.update()
            bullet.render(self.display, offset=render_scroll)
            if bullet.rect().colliderect(self.player.rect()):
                if self.player.explode():
                    self.status = "menu"
            tilesAround = self.game.tilemap.physics_rect_around(bullet.pos)
            self.handle_tiles_around(tilesAround,bullet,enemy)
    def handle_tiles_around(self, tilesAround,bullet,enemy):
        for tile in tilesAround:
            if bullet.rect().colliderect(tile[0]) or bullet.distance_traveled >= 400:
                if bullet in enemy.sended_Bullet:
                    enemy.sended_Bullet.remove(bullet)
    #gère tout les évènements du clavier et leurs actions associées
    def handle_pygame_events(self):
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
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
                    self.status = "main"
                    self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.movement[0] = True + self.player.playerSpeed
                if event.key == pygame.K_d:
                    self.movement[1] = True + self.player.playerSpeed
                if event.key == pygame.K_e and self.player.canDash and self.movement[0] > 0:
                    self.player.isDashingLeft = True
                if event.key == pygame.K_e and self.player.canDash and self.movement[1] > 0:
                    self.player.isDashingRight = True
                if event.key == pygame.K_SPACE and self.player.isJumping == False:
                    self.player.velocity[1] = self.player.jumpPower
                    self.player.isJumping = True
                if event.key == pygame.K_SPACE and self.player.isWallJumping:
                    self.player.velocity[1] = self.player.jumpPower
                    self.player.isWallJumping -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.player.is_attacking:
                        self.player.is_attacking = True
                        self.player.attack_timer = int(0.5 * 60)
                        sound = pygame.mixer.Sound("SONG/player_attack.mp3")
                        sound.play()
                    for enemy in self.ennemies:
                        distance_x = abs(self.player.pos[0] - enemy.pos[0])
                        distance_y = abs(self.player.pos[1] - enemy.pos[1])
                        if distance_x < 30 and distance_y < 10:
                            enemy.hurt(self.player.dammages)
                            self.ennemies.remove(enemy)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
            



