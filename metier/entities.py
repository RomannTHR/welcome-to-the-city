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
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x


        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self.isOnGround = True
                    self.isJumping = False
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
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
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run') 
        else:
            self.set_action('idle')