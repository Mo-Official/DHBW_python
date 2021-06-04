from typing import Tuple
import pygame as pg
from pygame import Rect, Surface, font
from settings import *
import functools

def draw_text(surface:Surface, text: str, coord:Tuple[int,int]=(0,0), size=16, color=WHITE, stretch_surface=True) -> None:
    used_font:font.Font = font.Font(pg.font.match_font(FONT_ARIAL), size)
    text_surface: Surface = used_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = coord[0]
    text_rect.y = coord[1]
    surface_rect :Rect = surface.get_rect()
    
    # make the surface bigger, if the text_rect is bigger
    if stretch_surface:
        if text_rect.width>surface_rect.width:
            surface.get_width
            surface_rect.width = text_rect.width
        if text_rect.height>surface_rect.height:
            surface_rect.height = text_rect.height

    surface.blit(text_surface, text_rect)

def print_log(msg, mode="INFO"):
    if LOGGING:
        print("\n",mode,":",msg)



def debug(func, debug=True):
    """
    Print the function signature and return value
    SOURCE: https://realpython.com/primer-on-python-decorators/#debugging-code"""
    if CALLS_DEBUG:
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args_repr = [repr(a) for a in args]                      # 1
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
            signature = ", ".join(args_repr + kwargs_repr)           # 3
            print_log(f"CALLEING {func.__name__}({signature})")
            value = func(*args, **kwargs)
            print_log(f"{func.__name__!r} RETURNED {value!r}")           # 4
            return value
        return wrapper_debug

