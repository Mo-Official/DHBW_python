import functools
from typing import Tuple

import pygame as pg
from pygame import Surface

from settings import CALLS_DEBUG, LOGGING, RED

__doc__ = """
    Author: Mouaz Tabboush

    util - A collection of utility functions
    ========================================

    util is a script containing functions used for debugging the game.

    Requirements
    ============

    * pygame
    * functools
    * typing.Tuple
    * settings.CALLS_DEBUG
    * settings.LOGGING
    * settings.RED
"""

def print_log(msg, mode="INFO"):
    if LOGGING:
        print("\n",mode,":",msg)

def debug(func):
    """
    Print the function signature and returns value
    SOURCE: https://realpython.com/primer-on-python-decorators/#debugging-code"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        if CALLS_DEBUG:
            print_log(f"CALLEING {func.__name__}({signature})")
        value = func(*args, **kwargs)
        if CALLS_DEBUG:
            print_log(f"{func.__name__!r} RETURNED {value!r}")           # 4
        return value
    return wrapper_debug

    
def get_outline(image: Surface, color: Tuple[int,int,int]=RED)->Surface:
    """
    Returns an outlined image of the same size.
    
    the image argument must either be a convert surface with a set colorkey, or a convert_alpha surface.
    
    color is the color which the outline will be drawn.
    
    SOURCE: https://pastebin.com/XXRngMZh
    """
    rect = image.get_rect()
    mask = pg.mask.from_surface(image)
    outline = mask.outline()
    outline_image = pg.Surface(rect.size).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    for point in outline:
        outline_image.set_at(point, color)
    return outline_image

