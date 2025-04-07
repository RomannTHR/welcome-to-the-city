import pygame
import random
from utils.utils import load_png
from metier.projectile import Projectile
class PhysicsEntities:
    def __init__(self, game, e_type, pos, size,dammages = 4):
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


    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[0])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement = (0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0] 

        entity_rect = self.rect()
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
                        if direction == 'y':
                            self.pos = [self.pos[0] , self.pos[1]]
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


        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()
        self.checkLowPosition()
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
    def checkLowPosition(self):
        if self.pos[1]>=640:
            self.pos = [100,50]
class  Enemy(PhysicsEntities):
    def __init__(self,game,pos,size,start,end):
        self.image, self.bullet_rect = load_png("Bullets/bullet.png")
        super().__init__(game,'enemy',pos,size)
        new_size =(200,200)
        self.image = pygame.transform.scale(self.image, new_size)
        self.walking = 0
        self.start = start
        self.pos[0] = pos[0]
        self.end = end
        self.speed = 2
        self.direction = -1
        self.sended_Bullet = []
        self.can_fire = 0
    def update(self, tilemap, movement=(0, 0)):
        self.pos[0] += self.direction*self.speed
        self.can_fire-=1
        distance_x = abs(self.pos[0] - self.game.player.pos[0])
        if distance_x < 300 and self.can_fire <= 0:
            dx = self.game.player.pos[0] - self.pos[0]
            dy = self.game.player.pos[1] - self.pos[1]
            dist = max((dx**2 + dy**2) ** 0.5, 1)

            direction = (dx / dist, dy / dist)
            bullet = Projectile(self.pos[0], self.pos[1], direction)
            self.sended_Bullet.append(bullet)
            self.can_fire = 180

        if self.pos[0] <= self.start and self.direction == -1:
            self.direction = 1
        elif self.pos[0] >= self.end and self.direction == 1:
            self.direction = -1
        for bullet in self.sended_Bullet:
            bullet.update()




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
        

    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.canDash = True
            self.wallJumping = 1
        


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