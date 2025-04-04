import json
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1,0), (0,1)])) : 0,
    tuple(sorted([(1,0), (0,1), (-1,0)])) : 1,
    tuple(sorted([(-1,0), (0,1)])) : 2,
    tuple(sorted([(-1,0), (0,-1), (0,1)])) : 3,
    tuple(sorted([(-1,0), (0,-1)])) : 4,
    tuple(sorted([(-1,0), (0,-1), (1,0)])) : 5,
    tuple(sorted([(-1,0), (0,-1)])) : 6,
    tuple(sorted([(1,0), (0,-1), (0, 1)])) : 7,
    tuple(sorted([(1,0), (-1,0), (0,1), (0, -1)])) : 8,
}

NEIGHTBOR_OFFSETS = [(1,0), (1,1), (1,-1), (0,1), (0,-1), (0,0), (-1,1), (-1,-1), (-1,0)] #Utile pour détecter toutes les potentielles entitées autour de notre entité 
PHYSICS_TILES = {'grass','stone', 'plateforme'}
AUTOTILE_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []


    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), (int(pos[1] // self.tile_size)))
        for offset in NEIGHTBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size,self.tile_size,self.tile_size))
        return rects
    
    def all_physics_rect(self):
        rects = []
        for key in self.tilemap:
            tile = tile[key]
            print(tile['pos'])
        return rects
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid' : self.offgrid_tiles}, f)
        f.close()


    def load(self, path):
        f = open(path, 'r')
        data = json.load(f)
        f.close()
        
        self.tilemap = data['tilemap']
        self.tilemap_size = data['tile_size']
        self.offgrid_tiles = data['offgrid']

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neightbors = set()
            for shift in [(1,0), (-1,0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neightbors.add(shift)
            neightbors = tuple(sorted(neightbors))
            if(tile['type'] in AUTOTILE_TILES) and (neightbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neightbors]

    def render(self, surf, offset=(0,0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))