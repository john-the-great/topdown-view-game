import pygame, os
from math import sqrt 

class Player:
    def __init__(self):
        self.rect = pygame.Rect(67, 34, 16, 16)
        self.image = {
            'run_right':[], 'run_left':[], 'run_up':[], 'run_down':[],
            'idle_right':[], 'idle_left':[], 'idle_up':[], 'idle_down':[]
        }
        self.image_id = 0
        self.curr_mov = 'idle_down'
        self.pre_direction = 'down'
        #Load images
        path = 'images/'
        for name in os.listdir(path):
            surf = pygame.image.load((path + name))
            mov_name = ''
            for char in name:
                if char.isdigit():
                    break
                mov_name += char
            self.image[mov_name].append(surf)
        self.pos = [self.rect.x, self.rect.y]
        self.vels = [0, 0]
        self.movement_speed = 1

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        #reset values
        self.vels = [0, 0]
        self.curr_mov = self.pre_direction

        if keys[pygame.K_w]:
            self.vels[1] = self.movement_speed * -1
            self.curr_mov = 'run_up'
            self.pre_direction = 'up'
        elif keys[pygame.K_s]:
            self.vels[1] = self.movement_speed
            self.curr_mov = 'run_down'
            self.pre_direction = 'down'

        if keys[pygame.K_d]:
            self.vels[0] = self.movement_speed
            self.curr_mov = 'run_right'
            self.pre_direction = 'right'
        elif keys[pygame.K_a]:
            self.vels[0] = self.movement_speed * -1
            self.curr_mov = 'run_left'
            self.pre_direction = 'left'

        if not (self.vels[0] != 0 and self.vels[1] != 0):
            self.pos[0] += self.vels[0] * dt
            self.pos[1] += self.vels[1] * dt
        else:
            #slow down for diagonal movement
            if self.vels[0] > -1 and self.vels[1] > -1:
                speed = sqrt((self.vels[0] + self.vels[1])) / 2
                self.vels = [speed, speed]
            elif self.vels[0] > -1 and self.vels[1] < 0:
                speed = sqrt((self.vels[0] + self.vels[1]*-1)) / 2
                self.vels = [speed, speed*-1]
            elif self.vels[0] < 0 and self.vels[1] > -1:
                speed = sqrt((self.vels[0]*-1 + self.vels[1])) / 2
                self.vels = [speed*-1, speed]
            elif self.vels[0] < 0 and self.vels[1] < 0:
                speed = sqrt((self.vels[0]*-1 + self.vels[1]*-1)) / 2
                self.vels = [speed*-1, speed*-1]
            self.pos[0] += self.vels[0] * dt
            self.pos[1] += self.vels[1] * dt
        
        #update player rect
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def animate(self, surf, dt):
        try: player_image = self.image[self.curr_mov][int(self.image_id)]
        except: player_image = self.image['idle_' + self.curr_mov][int(self.image_id)]
        if self.image_id >= 2.7:
            self.image_id = 0
        self.image_id += 0.1 * dt
        surf.blit(player_image, (
            self.rect.x, self.rect.y
        ))