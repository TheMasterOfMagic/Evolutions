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
        Bar(self)

    def get_rgb(self):
        return self.rgb

    def get_food_number(self):
        return self.food_number


class Bar:
    bars = []
    next_id = 1

    def __init__(self, camp):
        Bar.bars.append(self)
        self.id = Bar.next_id
        Bar.next_id += 1

        self.x = BAR_BLOCK_X*self.id
        self.y = BAR_BLOCK_Y
        self.w = BAR_BLOCK_WIDTH
        self.unit_h = 1/5
        self.camp = camp
        self.data = camp.get_food_number

    def get_rgb(self):
        return self.camp.get_rgb()

    def render(self):
        h = self.data()*self.unit_h
        h = max(h, 0.1)
        rect = pygame.Rect(self.x*BLOCK_SIZE, (self.y-h)*BLOCK_SIZE, self.w*BLOCK_SIZE, h*BLOCK_SIZE)
        pygame.draw.rect(DISPLAYSURFACE, self.get_rgb(), rect)


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


TIMER_ELAPSE = 50
# ================
MAP_WIDTH = 20
MAP_HEIGHT = 20
OBSTACLE_FACTOR = 0.1
OBSTACLE_TYPE = "salt"
FOOD_NUMBER = 3
REACHING_FOOD_CORRECTION_FACTOR = 10000
INFINITE_DISTANCE = MAP_WIDTH + MAP_HEIGHT
MAX_SEARCHING_DISTANCE = 5
# ================
BLOCK_SIZE = int(600/max(1.5*MAP_WIDTH, MAP_HEIGHT))
BLOCK_EDGE_WIDTH = 1
BLOCK_EDGE_RGB = 0, 255, 255
FOOD_RGB = 0, 255, 0
MAP_BLOCK_X = 4
MAP_BLOCK_Y = 1
SCREEN_BLOCK_WIDTH = MAP_WIDTH+5
SCREEN_BLOCK_HEIGHT = MAP_HEIGHT+2
BAR_BLOCK_X = 1
BAR_BLOCK_Y = MAP_BLOCK_Y+MAP_HEIGHT
BAR_BLOCK_WIDTH = 1

pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((SCREEN_BLOCK_WIDTH*BLOCK_SIZE,
                                          SCREEN_BLOCK_HEIGHT*BLOCK_SIZE))
