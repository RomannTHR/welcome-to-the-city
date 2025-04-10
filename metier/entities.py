import pygame
import random
from utils.utils import load_png
from metier.projectile import Projectile
class PhysicsEntities:
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
        self.just_jumped_from_jumper = False


    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement = (0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0] 

        entity_rect = self.rect()

        #Manage collisions with physics entities
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                if frame_movement[0] > 0:
                    entity_rect.right = rect[0].left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect[0].right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                if frame_movement[1] > 0:
                    is_moving = rect[1]['ismoving']
                    if is_moving and self.isOnGround:
                        direction = rect[1]['direction']
                        if direction == 'x':
                            self.pos = [self.pos[0] + (rect[1]['next_pos_increment'] * 32//10) , self.pos[1]]
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


        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        if not self.just_jumped_from_jumper:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)

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
        
    def update(self, tilemap,player_pos0,player_pos1, movement=(0, 0)):
        self.pos[0] += self.direction*self.speed
        self.can_fire-=1
        self.set_action('idle')
        distance_x = abs(self.pos[0] - player_pos0)
        if distance_x < 100 and self.can_fire <= 0:
            self.shoot(player_pos0, player_pos1)
        if self.pos[0] <= self.start and self.direction == -1:
            self.direction = 1
            self.flip = False
        elif self.pos[0] >= self.end and self.direction == 1:
            self.direction = -1
            self.flip = True
        for bullet in self.sended_Bullet:
            bullet.update()
        self.animation.update()
    def shoot(self, player_pos0, player_pos1):
        dx = player_pos0 - self.pos[0]
        dy = player_pos1 - self.pos[1]
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

        
        #PowerUp
        self.isShielded = False
        self.jumpPower = -3.5
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
            else:
                self.set_action('run')
                super().update(tilemap, movement=(0, 0))
                return

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
            self.set_action('jump')
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
        elif movement[0] != 0:
            self.set_action('run') 
        else:
            self.set_action('idle')
        #Manage collisions with Items entities
        for rect in tilemap.items_rects_around(self.pos):
            if self.rect().colliderect(rect[0]):
                if rect[1]['item_name'] == 'cartes':
                    self.map_number += 1
                    del tilemap.tilemap[str(rect[1]['data']['pos'][0]) + ';' + str(rect[1]['data']['pos'][1])]

    def checkLowPosition(self):
        if self.pos[1]>=640:
            return True
    def explode(self):
        self.game.initialPosition = [100,50]
        self.pos = self.game.initialPosition
        self.velocity = [0, 0]
        self.life+=5
        self.jumpPower = -3.5
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.set_action('idle')
        sound = pygame.mixer.Sound("SONG/start.mp3")
        sound.play()
        return True
    def attack(self):
        return self.dammages



