import pygame
import random
from utils.utils import load_png
from metier.projectile import Projectile

NEIGHTBOR_OFFSETS = [(1,0), (1,1), (1,-1), (0,1), (0,-1), (0,0), (-1,1), (-1,-1), (-1,0)] #Utile pour détecter toutes les potentielles entitées autour de notre entité 

class PhysicsEntities:

    """
    Classe qui représente toutes les entitées de la map ex : Player, Monstres, Ennemis...
    """

    def __init__(self, game, e_type, pos, size,dammages = 5):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.dammages = dammages
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.life = 5
        self.attack_timer = 0
        self.is_attacking = False
        self.is_on_moving_plateform = False
        self.just_jumped_from_jumper = False
        self.counter = 0


    def rect(self):
        
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[0])

    def set_action(self, action):
        """
        Defini une action / une animation à faire par l'entité (ex: Courir, Marcher, Attendre, Sauter...)
        """
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement = (0, 0)):

        """
        Va gérer les collisions de l'entité avec la map, les déplacements...
        """


        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0] 

        entity_rect = self.rect()

        

        #Manage collisions with physics entities
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                if frame_movement[0] > 0 and not self.is_on_moving_plateform:
                    entity_rect.right = rect[0].left
                    self.collisions['right'] = True
                if frame_movement[0] < 0 and not self.is_on_moving_plateform:
                    #print("test")
                    entity_rect.left = rect[0].right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                if frame_movement[1] > 0:
                    is_moving = rect[1]['ismoving']
                    if not is_moving and self.isOnGround:
                        self.is_on_moving_plateform = False
                    elif is_moving and self.isOnGround:
                        direction = rect[1]['direction']
                        if direction == 'x':
                            self.pos = [self.pos[0] + (rect[1]['next_pos_increment']) , self.pos[1]]
                    
                    if rect[1]['data']['type'] == 'jumper':
                        self.velocity[1] = -15
                        self.just_jumped_from_jumper = True
                    self.isOnGround = True
                    self.isJumping = False
                    entity_rect.bottom = rect[0].top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect[0].bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        for rect in tilemap.pixel_moving_platforms_around(self.pos):
            if rect[1]['ismoving'] == True:
                self.is_on_moving_plateform = True


        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        if not self.just_jumped_from_jumper:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)
            self.counter+=1
            if self.counter == 60:
                self.counter = 0

        if (self.collisions['down'] or self.collisions['up']) and not self.just_jumped_from_jumper:
            self.velocity[1] = 0

        self.just_jumped_from_jumper = False
        self.animation.update()


    def render(self, surf, offset=(0,0)):
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
    
    def hurt(self,degats):
        if degats <= self.life :
            self.life-=degats
        else:
            self.explode()
    def explode(self):
        """
        Fais mourir l'entité (notamment le joueur)
        """
        self.game.initialPosition = [100,50]
        self.pos = self.game.initialPosition
        self.velocity = [0, 0]
        self.life+=5
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.set_action('idle')

class  Enemy(PhysicsEntities):
    def __init__(self,game,pos,size,start,end):
        self.image, self.bullet_rect = load_png("Bullets/bullet.png")
        super().__init__(game,'enemy',pos,size)
        self.walking = 0
        self.start = start
        self.pos[0] = pos[0]
        self.end = end
        self.speed = 2
        self.direction = -1
        self.sended_Bullet = []
        self.can_fire = 0
        self.set_action('idle')
        
    def update(self, tilemap, movement=(0, 0)):
        """
        Va gérer les projectiles, les collisions avec les balles...
        """
        self.pos[0] += self.direction*self.speed
        self.can_fire-=1
        self.set_action('idle')
        distance_x = abs(self.pos[0] - self.game.player.pos[0])
        if distance_x < 300 and self.can_fire <= 0:
            self.shoot()
        if self.pos[0] <= self.start and self.direction == -1:
            self.direction = 1
            self.flip = False
        elif self.pos[0] >= self.end and self.direction == 1:
            self.direction = -1
            self.flip = True
        for bullet in self.sended_Bullet:
            bullet.update()
        self.animation.update()
    def shoot(self):
        """
        Fonction qui fait tirer l'ennemi
        """
        dx = self.game.player.pos[0] - self.pos[0]
        dy = self.game.player.pos[1] - self.pos[1]
        #made with chatgpt
        dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        direction = (dx / dist, dy / dist)
        #
        bullet = Projectile(self.pos[0], self.pos[1], direction)
        self.sended_Bullet.append(bullet)
        self.can_fire = 180


class Player(PhysicsEntities):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.isOnGround = False
        self.isJumping = False

        #Dashing
        self.isDashingRight  = False
        self.isDashingLeft = False
        self.canDash = True
        self.dashTimer = 0
        self.dashSpeed = 10
        
        #Wall Jump

        self.isWallJumping = False
        self.wallJumping = 1

        #Player Settings
        self.playerSpeed = 0.5

        #Achivements

        self.map_number = 0

        
        #HPs
        self.max_life = 5
        self.life = 5


        #PowerUp
        self.isShielded = False
        self.jumpPower = -3.5
        
    def render(self, surf, offset=(0,0)):
        super().render(surf,offset)
        bar_width = 25
        bar_height = 3
        hp_percent = max(self.life / self.max_life, 0)
        bar_x = self.pos[0] - offset[0] + self.anim_offset[0] + 2.5
        bar_y = self.pos[1] - offset[1] + self.anim_offset[1] - 10 

        pygame.draw.rect(surf, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        pygame.draw.rect(surf, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_percent), bar_height))

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.checkLowPosition()
        self.air_time += 1
        

        if self.collisions['down']:
            self.air_time = 0
            self.canDash = True
            self.wallJumping = 1
            if self.life>5:
                self.isShielded = True
            else:
                self.isShielded = False


        if self.collisions['right'] or self.collisions['left']:
            if self.wallJumping > 0:
                self.isWallJumping = True
                self.wallJumping -= 1


        if self.air_time > 4:
            if self.is_attacking:
                self.set_action('attack')
            else:
                self.set_action('jump')
        elif self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
            else:
                self.set_action('attack')
        elif movement[0] != 0:
            self.set_action('run') 
        else:
            self.set_action('idle')
        
        
        if self.dashTimer >= 10:
            self.isDashingRight = False
            self.isDashingLeft = False
            self.velocity[0] = 0
            self.dashTimer = 0
        if self.isDashingRight:
            self.velocity[0] = self.dashSpeed
            self.dashTimer += 1
            self.canDash = False
        if self.isDashingLeft:
            self.velocity[0] = -self.dashSpeed
            self.dashTimer += 1
            self.canDash = False
        

        #Manage collisions with Items entities
        for rect in tilemap.items_rects_around(self.pos):
            if self.rect().colliderect(rect[0]):
                if rect[1]['item_name'] == 'cartes':
                    self.map_number += 1
                    del tilemap.tilemap[str(rect[1]['data']['pos'][0]) + ';' + str(rect[1]['data']['pos'][1])]


    def checkLowPosition(self):
        if self.pos[1]>=640:

            self.explode()
    def explode(self):
        self.game.initialPosition = [100,50]
        self.pos = self.game.initialPosition
        self.velocity = [0, 0]
        self.life = 5
        self.jumpPower = -3.5
        self.set_action('idle')
        sound = pygame.mixer.Sound("SONG/start.mp3")
        sound.play()
        return True
    def attack(self):
        return self.dammages

class FinalBoss(PhysicsEntities):
    """
    Cette classe représente le boss final présent à la fin du niveau 1
    """
    def __init__(self, game, pos, size):
        super().__init__(game, 'finalboss', pos, size)

        self.physics_pos = [self.pos[0] + (self.size[0] - 32) // 2, self.pos[1] + (self.size[1] - 32)]
        self.movement_range_x = (-668,-228)

        self.movement = [False, False]
        self.hitbox_size = (32, 32)

        self.is_spawning = False
        self.spawn_duration = 2*60
        self.spawn_timer = 0

        self.death_timer = 0
        self.is_dying = False
        self.is_dead = False

        self.is_attacking = False
        self.wait_attack_timer = 2*60
        self.attack_duration = 1*60 #1 seconde
        self.attack_timer = 1*60
        self.set_action('idle')

        #Paramètrs du boss
        self.max_life = 100
        self.life = 100




    def rect(self):
        return pygame.Rect(self.physics_pos[0], self.physics_pos[1], self.hitbox_size[0], self.hitbox_size[0])

        
    def check_finalboss_in_the_screen(self, player_pos):
        """
        Regarde si le boss est apparu dans sur l'écran
        """
        for offset in NEIGHTBOR_OFFSETS:
            finalboss_position = (int(self.physics_pos[0] // 32),int(self.physics_pos[1] // 32))
            check_loc = (finalboss_position[0] + (offset[0] + (20//2)), finalboss_position[1] + (offset[1] + (14//2)))
            tile_player_pos = (int(player_pos[0] // 32), int(player_pos[1] // 32))
            if tile_player_pos[0] == check_loc[0] and abs(tile_player_pos[1] - check_loc[1]) <= 5:
                self.is_spawning = True
                self.spawn_timer = self.spawn_duration

    def check_player_around(self, player_pos):
        """
        Regarde si le joueur est proche du boss
        """
        for offset in NEIGHTBOR_OFFSETS:
            finalboss_position = (int(self.physics_pos[0] // 32),int(self.physics_pos[1] // 32))
            check_loc = (finalboss_position[0] + offset[0], finalboss_position[1] + offset[1])
            tile_player_pos = (int(player_pos[0] // 32), int(player_pos[1] // 32))
            if tile_player_pos == check_loc:
                self.wait_attack_timer -= 1
                if self.wait_attack_timer <= 0:
                    self.attack_timer = self.attack_duration
                    self.is_attacking = True
                    self.wait_attack_timer = 60
            

    def update(self, tilemap, player, movement=(0,0)):
        """
        Gère les collisions et les animations du boss
        """

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        player_pos = player.pos
        if not self.is_dying:
            if player_pos[0] > self.physics_pos[0]:
                direction = 1
            elif player_pos[0] < self.physics_pos[0]:
                direction = -1
            else:
                direction = 0
        else:
            direction = 0

        if direction != 0:
            if (direction == -1 and self.physics_pos[0] > self.movement_range_x[0]) or \
            (direction == 1 and self.physics_pos[0] < self.movement_range_x[1]):
                self.movement[0] = direction
            else:
                self.movement[0] = 0
        else:
            self.movement[0] = 0
        
        frame_movement = (self.movement[0] + self.velocity[0], self.movement[1] + self.velocity[1])
        self.physics_pos[0] += frame_movement[0] 

        entity_rect = self.rect()

        


        #Manage collisions with physics entities
        for rect in tilemap.physics_rect_around(self.physics_pos):
            if entity_rect.colliderect(rect[0]):
                if frame_movement[0] > 0:
                    entity_rect.right = rect[0].left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect[0].right
                    self.collisions['left'] = True
                self.physics_pos[0] = entity_rect.x

        self.physics_pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.physics_pos):
            if entity_rect.colliderect(rect[0]):
                if frame_movement[1] > 0:
                    self.isOnGround = True
                    self.isJumping = False
                    entity_rect.bottom = rect[0].top
                    self.collisions['down'] = True
                elif frame_movement[1] < 0:
                    entity_rect.top = rect[0].bottom
                    self.collisions['up'] = True
                self.physics_pos[1] = entity_rect.y



        if self.movement[0] > 0:
            self.flip = False
        if self.movement[0] < 0:
            self.flip = True

        if not self.just_jumped_from_jumper:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)
            self.counter+=1
            if self.counter == 60:
                self.counter = 0

        if (self.collisions['down'] or self.collisions['up']) and not self.just_jumped_from_jumper:
            self.velocity[1] = 0

        self.just_jumped_from_jumper = False
        self.animation.update()

        self.check_player_around(player_pos)
        self.check_finalboss_in_the_screen(player_pos)


        player_rect = player.rect()
        finalboss_rect = self.rect()
        if player.is_attacking and player.attack_timer == 15:
            if finalboss_rect.colliderect(player_rect):
                self.life -= 5
                if self.life <= 0:
                    self.is_dying = True
                    self.death_timer = 360/2
                    keys_to_remove = [key for key, tile in tilemap.tilemap.items() if tile.get('type') == 'invisible']
                    for key in keys_to_remove:
                        del tilemap.tilemap[key]




        if self.is_attacking and not self.is_dying:
            self.attack_timer -= 1
            if self.attack_timer == self.attack_duration//2:
                #Check if the player rect collide with the boss rect, if yes, then apply boss damage
                if finalboss_rect.colliderect(player_rect):
                    player.life -= 1

                    if player.life == 0:
                        player.explode()

            if self.attack_timer <= 0:
                self.is_attacking = False
            else:
                self.set_action('attack')
        elif self.is_spawning and not self.is_dying:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.is_spawning = False
            else:
                self.set_action('spawning')
        elif self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.is_dying = False
                self.is_dead = True
                self.game.finalboss = None
            else:
                self.set_action('death')
        else:
            self.set_action('idle')


        self.animation.update()

    def explode(self):
        """
        Fais mourir le boss
        """
        self.set_action('death')


    def render(self, surf, offset):
        """
        Affiche le boss et sa barre de vie
        """
        draw_x = self.physics_pos[0] - (self.size[0] - self.hitbox_size[0]) // 2
        draw_y = self.physics_pos[1] - (self.size[1] - self.hitbox_size[1]) + 16

        #Aide de ChatGPT pour la barre d'hp
        bar_width = 50
        bar_height = 6
        hp_percent = max(self.life / self.max_life, 0)


        bar_x = self.physics_pos[0] - offset[0] - 10
        bar_y = self.physics_pos[1] - offset[1] - 50 

        pygame.draw.rect(surf, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        pygame.draw.rect(surf, (255, 0, 0), (bar_x, bar_y, int(bar_width * hp_percent), bar_height))


        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (draw_x - offset[0], draw_y - offset[1]))
