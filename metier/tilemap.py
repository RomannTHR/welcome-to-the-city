import json
import pygame


NEIGHTBOR_OFFSETS = [(1,0), (1,1), (1,-1), (0,1), (0,-1), (0,0), (-1,1), (-1,-1), (-1,0)] #Utile pour détecter toutes les potentielles entitées autour de notre entité 
PHYSICS_TILES = {'grass','stone', 'plateforme', 'ice', 'purplegrass', 'jumper'}
ITEMS_TILES = {'cartes'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.moving_tiles = []


    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), (int(pos[1] // self.tile_size)))
        for offset in NEIGHTBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            check_loc_int = (tile_loc[0] + offset[0] , tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
            for tile in self.moving_tiles:
                check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
                tile_x = int(tile['pos'][0]) 
                tile_y = int(tile['pos'][1])
                if (tile_x, tile_y) == check_loc:
                    tiles.append(tile)
        return tiles

    def physics_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                if 'move_delay' in tile:
                    rects.append((pygame.Rect(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size,self.tile_size,self.tile_size), {'ismoving':True, 'next_pos_increment': tile['next_pos_increment'], 'direction': tile['direction'], 'data': tile}))
                else:
                    rects.append((pygame.Rect(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size,self.tile_size,self.tile_size), {'ismoving':False, 'data': tile} ))
        return rects
    
    def items_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            str_type = tile['type'].split('/')
            tile_type = str_type[0]
            if tile_type == 'items':
                item_name = str_type[1]
                if item_name in ITEMS_TILES:
                    rects.append((pygame.Rect(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size,self.tile_size,self.tile_size), {'item_name' : item_name, 'data':tile}))
        return rects


    def all_physics_rect(self):
        rects = []
        for key in self.tilemap:
            tile = tile[key]
            print(tile['pos'])
        return rects
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid' : self.offgrid_tiles, 'moving_tiles' : self.moving_tiles}, f)
        f.close()


    def load(self, path):
        f = open(path, 'r')
        data = json.load(f)
        f.close()
        
        self.tilemap = data['tilemap']
        self.tilemap_size = data['tile_size']
        self.offgrid_tiles = data['offgrid']
        self.moving_tiles = data['moving_tiles']

    def update_tiles(self):
        for tile in self.moving_tiles:
            tile['frame_counter'] += 1

            if tile['frame_counter'] < tile.get('move_delay', 10):
                continue 

            tile['frame_counter'] = 0  
            initial_x, initial_y = tile['initial_pos']
            current_x, current_y = tile['pos']
            increment = tile['next_pos_increment']
            direction = tile.get('direction', 'x')
            range_limit = tile.get('range', 5) 
            if direction == 'x':

                delta = current_x - initial_x

                if abs(delta + increment) > range_limit:
                    tile['next_pos_increment'] *= -1
                    increment = tile['next_pos_increment']
                    
                tile['pos'] = (current_x + increment, current_y)

            elif direction == 'y':
                delta = current_y - initial_y

                if abs(delta + increment) > range_limit:
                    tile['next_pos_increment'] *= -1
                    increment = tile['next_pos_increment']

                tile['pos'] = (current_x, current_y + increment)


    def render(self, surf, offset=(0,0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for moving_tile in self.moving_tiles:
            surf.blit(self.game.assets[moving_tile['type']][moving_tile['variant']], (moving_tile['pos'][0] * self.tile_size - offset[0], moving_tile['pos'][1] * self.tile_size - offset[1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))