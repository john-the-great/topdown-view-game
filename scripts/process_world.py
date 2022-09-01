import chunk
from cmath import rect
import pygame
import json
import os
from random import randint

class MapC:
    def __init__(self, file_name, image_dir, processed_distances):
        self.data = json.load(open(file_name + '.json'))
        self.world_data = {}
        for key in self.data:
            image = pygame.image.load(image_dir + '/' + self.data[key]).convert()
            image.set_colorkey((0, 0, 0, 0))
            self.world_data[key] = [image, self.data[key], '1chunk']
        self.itterate_data = {}
        for id, key in enumerate(self.world_data):
            pos = key.split()
            pos1 = int(pos[0])
            pos2 = int(pos[1])
            self.itterate_data[id] = [pos1, pos2]
        self.sim_dis = processed_distances[0]
        self.x_dis = processed_distances[1]
        self.y_dis = processed_distances[2]

        self.data = json.load(open(file_name + '_transparent' + '.json'))
        self.folliage_data = {}
        for key in self.data:
            image = pygame.image.load(image_dir + '/' + self.data[key]).convert()
            image.set_colorkey((0, 0, 0, 0))
            self.folliage_data[key] = [image, self.data[key]]
        self.animated_water = True
        self.water_image_id = 0
        dir = 'images/world/water_animation'
        images = os.listdir(dir)
        sorted_ = []
        for name in images:
            for id, char in enumerate(name):
                if char.isdigit():
                    if name[id+1].isdigit():
                        sorted_.append(int(char + name[id+1]))
                        break
                    else:
                        sorted_.append(int(char))
                        break
        sorted_.sort()
        for id, num in enumerate(sorted_):
            sorted_[id] = 'water' + str(num) + '.png'
        self.water_animation = [pygame.image.load(dir + '/' + name) for name in sorted_]

    def convert_tile_size(self, TILE_SIZE):
        for key in self.world_data:
            self.world_data[key][0] = pygame.transform.scale(self.world_data[key][0], (TILE_SIZE, TILE_SIZE))
        self.TILE_SIZE = TILE_SIZE

    def convert_render_dis(
        self, x_dis: int, y_dis: int
    ):
        self.x_dis = x_dis
        self.y_dis = y_dis

        return self.x_dis, self.y_dis
    #if self.world_data[key][1] == 'grassShards2.png'

    def slice_chunks(self):
        positions = [[], []]
        for key in self.world_data:
            pos = key.split()
            x = int(pos[0])
            y = int(pos[1])
            positions[0].append(x)
            positions[1].append(y)
        tx = min(positions[0])
        ty = min(positions[1])
        width = abs(max(positions[0]) - tx)+self.TILE_SIZE
        height = abs(max(positions[1]) - ty)+self.TILE_SIZE

        tile_data = {}
        for wlength in range(width):
            x = tx+wlength
            for hlength in range(height):
                y = ty+hlength
                if x % self.TILE_SIZE == 0 and y % self.TILE_SIZE == 0:
                    has_data = False
                    for key in self.world_data:
                        if key == f'{x} {y}':
                            tile_data[key] = self.world_data[key]
                            has_data = True
                            break
                    if not has_data:
                        tile_data[f'{x} {y}'] = [None, None]

        chunk_data = {}
        marked = []
        for key in tile_data:
            tile_name = tile_data[key][1]
            try:
                # and tile_data[key][1] != 'tile.png'
                if tile_data[key][0] != None:
                    pos = key.split()
                    x = int(pos[0])
                    y = int(pos[1])
                    markedk = False
                    for marked_key in marked:
                        if marked_key == key:
                            markedk = True
                    if not markedk:
                        if not self.animated_water:
                            if tile_name == 'tile11.png':
                                if tile_data[f'{x+self.TILE_SIZE} {y}'][1] == tile_name and tile_data[f'{x} {y+self.TILE_SIZE}'][1] == tile_name and tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][1] == tile_name: 
                                    tmp_surf = pygame.Surface((self.TILE_SIZE*2, self.TILE_SIZE*2))
                                    tmp_surf.blit(tile_data[key][0], (0, 0))
                                    tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y}'][0], (self.TILE_SIZE, 0))
                                    tmp_surf.blit(tile_data[f'{x} {y+self.TILE_SIZE}'][0], (0, self.TILE_SIZE))
                                    tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][0], (self.TILE_SIZE, self.TILE_SIZE))
                                    marked.append(key)
                                    marked.append(f'{x+self.TILE_SIZE} {y}')
                                    marked.append(f'{x} {y+self.TILE_SIZE}')
                                    marked.append(f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}')
                                    chunk_data[key] = [tmp_surf, tile_data[key][1], '4chunk']
                                else:
                                    tile_data[key].append('1chunk')
                                    chunk_data[key] = tile_data[key]
                            else:
                                if tile_data[f'{x+self.TILE_SIZE} {y}'][1] != 'tile11.png' and tile_data[f'{x} {y+self.TILE_SIZE}'][1] != 'tile11.png' and tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][1] != 'tile11.png': 
                                    tmp_surf = pygame.Surface((self.TILE_SIZE*2, self.TILE_SIZE*2))
                                    tmp_surf.blit(tile_data[key][0], (0, 0))
                                    tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y}'][0], (self.TILE_SIZE, 0))
                                    tmp_surf.blit(tile_data[f'{x} {y+self.TILE_SIZE}'][0], (0, self.TILE_SIZE))
                                    tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][0], (self.TILE_SIZE, self.TILE_SIZE))
                                    marked.append(key)
                                    marked.append(f'{x+self.TILE_SIZE} {y}')
                                    marked.append(f'{x} {y+self.TILE_SIZE}')
                                    marked.append(f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}')
                                    chunk_data[key] = [tmp_surf, tile_data[key][1], '4chunk']
                                else:
                                    tile_data[key].append('1chunk')
                                    chunk_data[key] = tile_data[key]
                        else:
                            if tile_name != 'tile11.png':
                                if tile_data[f'{x+self.TILE_SIZE} {y}'][1] != 'tile11.png' and tile_data[f'{x} {y+self.TILE_SIZE}'][1] != 'tile11.png' and tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][1] != 'tile11.png':
                                    tmp_surf = pygame.Surface((self.TILE_SIZE*2, self.TILE_SIZE*2))
                                    tmp_surf.blit(tile_data[key][0], (0, 0))
                                    tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y}'][0], (self.TILE_SIZE, 0))
                                    tmp_surf.blit(tile_data[f'{x} {y+self.TILE_SIZE}'][0], (0, self.TILE_SIZE))
                                    tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][0], (self.TILE_SIZE, self.TILE_SIZE))
                                    marked.append(key)
                                    marked.append(f'{x+self.TILE_SIZE} {y}')
                                    marked.append(f'{x} {y+self.TILE_SIZE}')
                                    marked.append(f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}')
                                    chunk_data[key] = [tmp_surf, tile_data[key][1], '4chunk']
                                else:
                                    tile_data[key].append('1chunk')
                                    chunk_data[key] = tile_data[key]
                            else:
                                tile_data[key].append('1chunk')
                                chunk_data[key] = tile_data[key]
                else:
                    if tile_data[key][0] != None:
                        tile_data[key].append('1chunk')
                        chunk_data[key] = tile_data[key]
            except:
                tile_data[key].append('1chunk')
                chunk_data[key] = tile_data[key]

        self.world_data = chunk_data

        return pygame.Rect(x, y, width, height), tx, ty, width, height

    def slice_animated_chunks(self):
        positions = [[], []]
        for key in self.world_data:
            pos = key.split()
            x = int(pos[0])
            y = int(pos[1])
            positions[0].append(x)
            positions[1].append(y)
        tx = min(positions[0])
        ty = min(positions[1])
        width = abs(max(positions[0]) - tx)+self.TILE_SIZE
        height = abs(max(positions[1]) - ty)+self.TILE_SIZE

        tile_data = {}
        for wlength in range(width):
            x = tx+wlength
            for hlength in range(height):
                y = ty+hlength
                if x % self.TILE_SIZE == 0 and y % self.TILE_SIZE == 0:
                    has_data = False
                    for key in self.world_data:
                        if key == f'{x} {y}':
                            tile_data[key] = self.world_data[key]
                            has_data = True
                            break
                    if not has_data:
                        tile_data[f'{x} {y}'] = [None, None]

        marked = []
        for key in tile_data:
            tile_name = tile_data[key][1]
            try:
                # and tile_data[key][1] != 'tile.png'
                if tile_data[key][0] != None:
                    pos = key.split()
                    x = int(pos[0])
                    y = int(pos[1])
                    markedk = False
                    for marked_key in marked:
                        if marked_key == key:
                            markedk = True
                    if not markedk:
                        if tile_name == 'tile11.png':
                            if tile_data[f'{x+self.TILE_SIZE} {y}'][1] == tile_name and tile_data[f'{x} {y+self.TILE_SIZE}'][1] == tile_name and tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][1] == tile_name: 
                                marked.append(key)
                                marked.append(f'{x+self.TILE_SIZE} {y}')
                                marked.append(f'{x} {y+self.TILE_SIZE}')
                                marked.append(f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}')
                                self.world_data[key] = [tile_data[key][0], tile_data[key][1], '4chunk']
                                self.world_data[f'{x+self.TILE_SIZE} {y}'] = [tile_data[key][0], tile_data[key][1], '0chunk']
                                self.world_data[f'{x} {y+self.TILE_SIZE}'] = [tile_data[key][0], tile_data[key][1], '0chunk']
                                self.world_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'] = [tile_data[key][0], tile_data[key][1], '0chunk']
                else:
                    if tile_data[key][0] != None:
                        tile_data[key].append('1chunk')
                        self.world_data[key] = tile_data[key]
            except:
                tile_data[key].append('1chunk')
                self.world_data[key] = tile_data[key]

    def show_map(self, surf, player_pos, dt, scroll = [0, 0]):
        rect_list = []
        if self.animated_water:
            self.water_image_id += .04 * dt
            if self.water_image_id >= len(self.water_animation):
                self.water_image_id = 0
        for key in self.world_data:
            pos = key.split()
            x = int(pos[0])
            y = int(pos[1])
            if not self.world_data[key][0] == None:
                if abs(player_pos[0] - x-self.TILE_SIZE/2) < self.x_dis and abs(player_pos[1] - y-self.TILE_SIZE/2) < self.y_dis:
                    if not self.animated_water:
                        surf.blit(self.world_data[key][0], (x-scroll[0], y-scroll[1]))
                        #pygame.draw.rect(surf, (255, 255, 255), (
                        #   x-scroll[0], y-scroll[1], self.world_data[key][0].get_width(), self.world_data[key][0].get_height() 
                        #), 1)
                    else:
                        if self.world_data[key][1] != 'tile11.png':
                            surf.blit(self.world_data[key][0], (x-scroll[0], y-scroll[1]))
                        else:
                            surf.blit(self.water_animation[int(self.water_image_id)], (x-scroll[0], y-scroll[1]))
                if abs(player_pos[0] - x-self.TILE_SIZE/2) < self.sim_dis and abs(player_pos[1] - y-self.TILE_SIZE/2) < self.sim_dis:
                    if self.world_data[key][1] == 'tile11.png':
                        if self.world_data[key][2] == '4chunk':
                            rect_list.append(pygame.Rect(x, y, self.TILE_SIZE*2, self.TILE_SIZE*2))
                        elif self.world_data[key][2] == '1chunk':
                            rect_list.append(pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE))
                            
        return rect_list

    def show_folliage(self, surf, player_pos, rect_list, scroll):
        for key in self.folliage_data:
            pos = key.split()
            x = int(pos[0])
            y = int(pos[1])
            if abs(player_pos[0] - x-self.TILE_SIZE/2) < self.x_dis and abs(player_pos[1] - y-self.TILE_SIZE/2) < self.y_dis:
                surf.blit(self.folliage_data[key][0], (x-scroll[0], y-scroll[1]))
            if self.folliage_data[key][1] == 'tile24.png':
                if abs(player_pos[0] - x-self.TILE_SIZE/2) < self.sim_dis and abs(player_pos[1] - y-self.TILE_SIZE/2) < self.sim_dis:
                    rect_list.append(pygame.Rect(x+self.TILE_SIZE*1.4, y+self.TILE_SIZE*3, self.TILE_SIZE, self.TILE_SIZE))
        return rect_list
