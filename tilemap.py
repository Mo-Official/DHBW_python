from typing import Union
import pygame as pg
import pytmx
from pygame import Rect, Surface
from pygame.sprite import Sprite

from settings import CAM_POINT, HEIGHT, WIDTH
from util import print_log

__doc__ = """
    Author: Mouaz Tabboush

    tilemap - the module for loading map files created by Tiled
    ===========================================================

    Tiled is a Map editing file that is used in this project to generate tmx files, which are loaded as maps.

    The layout of the map and where each object is are saved inside the tmx file.

    The Script also contains the Camera class which applies offset to game objects.


    Requirements
    ============
    
    * pygame
    * pytmx     
"""


class TiledMap:
    """
    TiledMap - Object that hold map data from a tmx file.

    The class is based on the following tutorial:
    https://www.youtube.com/watch?v=QIXyj3WeyZM
    """
    def __init__(self, filename):
        """
        Tests
        -----
        * not passing a correct directory
        * not passing a string
        * missing variables
        * pytmx not imported
        """
        try:
            self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
            self.width = self.tmxdata.width * self.tmxdata.tilewidth
            self.height = self.tmxdata.height * self.tmxdata.tileheight
        except Exception:
            print_log("Failure while loading the map", "ERROR")
            print_log("Please make sure that no assets are missing from the game folder.", "ERROR")
            pg.quit()


    def render(self, surface:Surface):
        """renders the tiles from the Tiledmap on a given surface.

        Tests
        -----
        * not passing a surface
        * problem with local function tile_image"""
        tile_image = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_image(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,y * self.tmxdata.tileheight))

    def make_map(self) -> Surface:
        """A Wrapper function that returns a surface of the map.
        
        Tests
        -----
        * Problem with creating a surface
        * problem with render()
        * missing variables"""
        temp_surface = Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
        

class Camera:
    """
    An Object that controls the offset of objects on the map.

    The class is based on the following tutorial:
    https://www.youtube.com/watch?v=3zV2ewk-IGU
    """
    def __init__(self, width, height):
        """
        Parameters
        ----------
        width: width of the camera
        height: height of the camera
        
        Tests
        -----
        passing negative width
        passing negative height"""
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity:Union[Sprite,Rect]) -> Rect:
        """Moves the passed entity or rect by the calculated offset in `update()`
        
        Tests
        -----
        * passing an unsupported type of entity
        * passed sprites without a rect
        * missing camera rect"""
        if isinstance(entity, pg.sprite.Sprite):
            return entity.rect.move(self.camera.topleft)
        elif isinstance(entity, pg.Rect):
            return entity.move(self.camera.topleft)


    def update(self, target:Sprite):
        """Calculates the offset of the passed target
        
        Tests
        -----
        * missing gloable variables
        * target not having a rect
        * missing local variables of the object"""
        x = -target.rect.x + CAM_POINT[0]
        y = -target.rect.y + CAM_POINT[1]

        # limit side scrolling
        x = min(0, x) # left
        y = min(0, y) # top 
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # buttom
        self.camera = Rect(x, y, self.width, self.height)


