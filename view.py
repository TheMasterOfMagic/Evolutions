import pygame
import numpy as np


def start(screen_width, screen_height):
    pygame.init()
    global DISPLAYSURFACE
    DISPLAYSURFACE = pygame.display.set_mode((screen_width, screen_height))


def set_palettes(palettes):
    global PALETTES
    PALETTES = palettes


def render_blocks(blocks, block_size, map_block_x, map_block_y):
    surface = DISPLAYSURFACE

    for block in blocks:
        x, y = block.pos
        if block.item is not None:
            color = PALETTES[type(block.item) if block.item.tag is not "ant" else block.item.camp]
        else:
            color = np.float32((0,)*3)
            for odor_type, odor_quantity in block.odors.items():
                color += np.array(PALETTES[odor_type]) * odor_quantity / 1000
            color /= len(block.odors)
            color = np.int32(color)

        width = 0
        rect = pygame.Rect((map_block_x+x)*block_size, (map_block_y+y)*block_size, block_size, block_size)
        pygame.draw.rect(surface, color, rect, width)


def fill_black():
    DISPLAYSURFACE.fill((0, 0, 0))


def update():
    pygame.display.update()
