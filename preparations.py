import pygame
from random import *


class GameOverException(Exception):
    pass


class Camp:
    camps = []

    def __init__(self, rgb, food_number, ant_number):
        self.id = len(Camp.camps)
        Camp.camps.append(self)
        self.rgb = rgb
        self.food_number = food_number
        self.ant_number = ant_number

    def get_rgb(self):
        return self.rgb


class Bar:
    def __init__(self, x, y, w, unit_h, color, data):
        self.x, self.y = x, y
        self.w = w
        self.unit_h = unit_h
        self.color = color
        self.data = data

    def render(self):
        h = self.data()*self.unit_h
        rect = pygame.Rect(self.x, self.y-h, self.w, h)
        pygame.draw.rect(DISPLAYSURFACE, self.color, rect)


def get_random_rgb(s=2*255):
    if s > 3*255:
        raise RuntimeError
    min_r = max(0, s-2*255)
    max_r = min(s, 255)
    r = randint(min_r, max_r)
    min_g = max(0, s-r-255)
    max_g = min(s-r, 255)
    g = randint(min_g, max_g)
    b = s-r-g
    return r, g, b


TIMER_ELAPSE = 200
# ================
MAP_WIDTH = 25
MAP_HEIGHT = 10
OBSTACLE_NUMBER = 0.2
FOOD_NUMBER = 5
REACHING_FOOD_CORRECTION_FACTOR = 10
Camp((255, 0, 0), 0, 1)
Camp((255, 255, 0), 0, 1)
Camp((128, 0, 255), 0, 1)
# ================
BLOCK_SIZE = 40
BLOCK_EDGE_WIDTH = 1
BLOCK_EDGE_RGB = get_random_rgb()
FOOD_RGB = 0, 255, 0
MAP_BLOCK_X = 4
MAP_BLOCK_Y = 1
SCREEN_BLOCK_WIDTH = MAP_WIDTH+5
SCREEN_BLOCK_HEIGHT = MAP_HEIGHT+2

pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((SCREEN_BLOCK_WIDTH*BLOCK_SIZE,
                                          SCREEN_BLOCK_HEIGHT*BLOCK_SIZE))
