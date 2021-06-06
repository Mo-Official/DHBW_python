import functools
from typing import Tuple
from datetime import datetime

import pygame as pg
from pygame import Surface

from settings import CALLS_DEBUG, LOGGING_TO_CONSOLE, LOGGING_TO_FILE, LOG_INFO, RED

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
    """A wrapper function around print() and open().write()
    
    Parameters
    ----------
    msg: the string that should be written to the file,
    or logged to the console
    
    mode: a tag the is appended to the message.
    useful when handeling logs messages differently.

    Tests
    -----
    - passing none string objects as a msg
    - open("log.txt", "a") no having write permissions
    - if a global variable is missing
    
    """
    if not LOG_INFO and mode=="INFO":
        return

    if LOGGING_TO_CONSOLE:
        print("\n",mode,": ",msg)

    if LOGGING_TO_FILE:
        with open("log.txt", "a") as fh:
            if not mode=="STARTUP":
                    fh.write("\n"+mode+": "+msg)
            else:
                    fh.write("\n\n========================================")
                    fh.write(f"\n# {mode}: {msg} at {datetime.now().strftime('%H:%M:%S')} #")
                    fh.write("\n========================================")
            
        
    

def debug(func):
    """
    Print the function signature and returns value
    SOURCE: https://realpython.com/primer-on-python-decorators/#debugging-code
    
    Parameters
    ----------
    func: the function that is wrapped by the debug decorator

    Test
    ----
    general error.
    """
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

    Parameter
    ---------
    image: image to calculate its mask

    color: color of the calculated mask

    Test
    ----
    passing a none-surface as image
    passing a none-tuple as color
    passing a invalid color
    """
    rect = image.get_rect()
    mask = pg.mask.from_surface(image)
    outline = mask.outline()
    outline_image = pg.Surface(rect.size).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    for point in outline:
        outline_image.set_at(point, color)
    return outline_image

