import pygame

class PhysicsEntities:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')


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

    def render(self, surf, offset=(0,0)):
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


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