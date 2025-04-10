import json
import pygame


NEIGHTBOR_OFFSETS = [(1,0), (1,1), (1,-1), (0,1), (0,-1), (0,0), (-1,1), (-1,-1), (-1,0)] #Utile pour détecter toutes les potentielles entitées autour de notre entité 
PHYSICS_TILES = {'grass','stone', 'plateforme', 'ice', 'purplegrass', 'jumper', 'invisible'}
ITEMS_TILES = {'cartes'}

class Tilemap:
    #Tilemap basé sur une vidéo youtube : https://www.youtube.com/watch?v=2gABYM5M0ww&t=11420s
    """
    Classe qui va gérer toutes les textures de la map (îles, plateformes mobiles/immobiles/items...)
    """
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.moving_tiles = []


    def tiles_around(self, pos):
        """
        Va retourner toutes les textures autour d'une certaine position (basé sur la liste d'offset plus haut)
        """
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


    
    def pixel_moving_platforms_around(self, pos, radius=64):
        """Retourne les plateformes mobiles en pixel très proches de pos."""
        rects = []
        for tile in self.moving_tiles:
            tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tile_size, self.tile_size)
            if tile_rect.collidepoint(pos[0], pos[1]) or tile_rect.colliderect(
                pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
            ):
                rects.append((
                    tile_rect,
                    {
                        'ismoving': True,
                        'next_pos_increment': tile['next_pos_increment'],
                        'direction': tile['direction'],
                        'data': tile
                    }
                ))
        return rects

    def physics_rect_around(self, pos):
        """
        Va retourner toutes les textures physiques (avec les quelles il y a des collisions) en Rect
        """
        rects = []

        # Tiles sur grille
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                if 'move_delay' in tile:
                    rects.append((
                        pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),
                        {'ismoving': True, 'next_pos_increment': tile['next_pos_increment'], 'direction': tile['direction'], 'data': tile}
                    ))
                else:
                    rects.append((
                        pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),
                        {'ismoving': False, 'data': tile}
                    ))

        # Plateformes pixels
        rects.extend(self.pixel_moving_platforms_around(pos))

        return rects
    
    def items_rects_around(self, pos):
        """
        Retourne les rects des items à proximité d'une position
        """
        rects = []
        for tile in self.tiles_around(pos):
            str_type = tile['type'].split('/')
            tile_type = str_type[0]
            if tile_type == 'items':
                item_name = str_type[1]
                if item_name in ITEMS_TILES:
                    rects.append((pygame.Rect(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size,self.tile_size,self.tile_size), {'item_name' : item_name, 'data':tile}))
        return rects



    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def save(self, path):
        """
        Permet de sauvegarder dans l'editeur (editor.py)
        """
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid' : self.offgrid_tiles, 'moving_tiles' : self.moving_tiles}, f)
        f.close()


    def load(self, path):
        """
        Permet de charger la map (les tiles)
        """
        f = open(path, 'r')
        data = json.load(f)
        f.close()

        self.tilemap = data['tilemap']
        self.tilemap_size = data['tile_size']
        self.offgrid_tiles = data['offgrid']
        self.moving_tiles = data['moving_tiles']

    def update_tiles(self):
        """
        Permet de faire bouger les moving tiles sur l'axe y et x
        """
        for tile in self.moving_tiles:

            tile['frame_counter'] = 0
            initial_x, initial_y = tile['initial_pos']
            current_x, current_y = tile['pos']
            increment = tile['next_pos_increment']
            direction = tile['direction']
            range_limit = 5 * self.tile_size
            if direction == 'x':
                #Aide de ChatGPT pour cette étape
                delta = current_x - initial_x

                if abs(delta + increment) > range_limit:
                    tile['next_pos_increment'] *= -1
                    increment = tile['next_pos_increment']

                tile['pos'] = (current_x + increment, current_y)

            elif direction == 'y':
                #print(tile['pos'])
                delta = current_y - initial_y

                if abs(delta + increment) > range_limit:
                    tile['next_pos_increment'] *= -1
                    increment = tile['next_pos_increment']

                tile['pos'] = (current_x, current_y + increment)


    def render(self, surf, offset=(0,0)):
        """
        Permet d'afficher les tiles sur l'écran
        """
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for moving_tile in self.moving_tiles:
            surf.blit(self.game.assets[moving_tile['type']][moving_tile['variant']], (moving_tile['pos'][0] - offset[0], moving_tile['pos'][1] - offset[1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))