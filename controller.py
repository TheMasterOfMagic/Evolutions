from config import *
from models.block import *
from models.item import *
from models.camp import *
import view
import pygame
from pygame.locals import *
import sys


def start():
    Block.initialize(MAP_WIDTH, MAP_HEIGHT)
    view.start(SCREEN_WIDTH, SCREEN_HEIGHT)

    # gen obstacles
    Block.generate(Obstacle, 10)

    odor_types = [Food, Camp(2), Camp(2), Camp(2)]
    Block.set_odor_types(odor_types)
    rgb = [(192, 192, 192), (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)]
    palettes = dict(zip([Obstacle]+odor_types, rgb))
    view.set_palettes(palettes)

    for camp in Camp.get_camps():
        Block.generate(Ant, camp.ant_number, camp)

    timer = USEREVENT + 1
    view_timer = timer + 1
    pygame.time.set_timer(timer, TIMER_ELAPSE)
    pygame.time.set_timer(view_timer, TIMER_ELAPSE)

    while True:
        for event in pygame.event.get():
            if event.type == timer:
                Block.generate(Food, 10-Food.get_food_number())
                Item.items_act()
                Block.odors_spread()
            elif event.type == view_timer:
                view.fill_black()
                view.render_blocks(Block.get_blocks(), BLOCK_SIZE, MAP_BLOCK_X, MAP_BLOCK_Y)
                view.update()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    start()
