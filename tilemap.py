import pygame as pg
from settings import *
import pytmx

class TiledMap:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        tile_image = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_image(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
        

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        if isinstance(entity, pg.sprite.Sprite):
            return entity.rect.move(self.camera.topleft)
        elif isinstance(entity, pg.Rect):
            return entity.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + CAM_POINT[0]
        y = -target.rect.y + CAM_POINT[1]

        # limit scrolling
        x = min(0, x) # left
        y = min(0, y) # top 
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # buttom
        self.camera = pg.Rect(x, y, self.width, self.height)


