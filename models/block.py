from random import sample, random
import numpy as np


def rand(_min, _max):
    return _min + random()*(_max-_min)


class Block:
    __blocks_matrix = None  # type: list[list[Block]]
    __blocks = None  # type: set[Block]
    __accessible_positions = None  # type: set[tuple[int, int]]
    __map_width = None  # type: int
    __map_height = None  # type: int
    __odor_types = None  # type: set

    def __init__(self, pos):
        self.pos = pos
        self.item = None
        self.odors = dict()
        self.odors_inc = dict()
        Block.__blocks.add(self)
        Block.__accessible_positions.add(self.pos)

    @classmethod
    def odors_spread(cls):
        blocks = cls.get_blocks()
        for block in blocks:
            nearby_blocks = block.get_nearby_blocks()
            for odor_type in Block.__odor_types:
                source_block = max(nearby_blocks, key=lambda x: x.odors[odor_type])
                block.odors_inc[odor_type] = (source_block.odors[odor_type] - block.odors[odor_type]) * rand(0.45, 0.55)
        for block in blocks:
            for odor_type in Block.__odor_types:
                block.odors[odor_type] *= rand(0.75, 0.85)
                block.odors[odor_type] += block.odors_inc[odor_type]
                block.odors_inc[odor_type] = 0
                block.odors[odor_type] *= 0 if block.odors[odor_type] < 1 else 1

    @classmethod
    def set_odor_types(cls, odor_types):
        cls.__odor_types = odor_types
        for block in cls.get_blocks():
            for odor_type in cls.__odor_types:
                block.odors[odor_type] = 0
                block.odors_inc[odor_type] = 0

    def got_item(self, item):
        self.item = item
        Block.__accessible_positions.remove(self.pos)

    def lost_item(self):
        self.item = None
        Block.__accessible_positions.add(self.pos)

    @classmethod
    def initialize(cls, map_width, map_height):
        cls.__map_width, cls.__map_height = map_width, map_height
        cls.__blocks = set()
        cls.__accessible_positions = set()
        cls.__blocks_matrix = list(
            list(
                cls((x, y)) for y in range(map_height)
            ) for x in range(map_width)
        )

    @classmethod
    def get_block(cls, pos):
        x, y = pos
        return Block.__blocks_matrix[x][y] if 0 <= x < cls.__map_width and 0 <= y < cls.__map_height else None

    @staticmethod
    def get_blocks():
        return Block.__blocks

    @staticmethod
    def get_accessible_positions(k: int=1):
        return sample(Block.__accessible_positions, k)

    @staticmethod
    def generate(t: type, k: int, *args):
        accessible_positions = Block.get_accessible_positions(k)
        for pos in accessible_positions:
            t(Block.get_block(pos), *args)

    def get_nearby_blocks(self):
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
        nearby_positions = list(np.array(self.pos)+np.array(direction) for direction in directions)
        nearby_blocks = list(Block.get_block(pos) for pos in nearby_positions)
        nearby_blocks = list(block for block in nearby_blocks if block is not None)
        return nearby_blocks

    def get_accessible_nearby_blocks(self):
        nearby_blocks = self.get_nearby_blocks()
        accessible_nearby_blocks = list(block for block in nearby_blocks if block.item.tag is not "obstacle")
        return accessible_nearby_blocks

    def get_empty_nearby_blocks(self):
        nearby_blocks = self.get_nearby_blocks()
        empty_nearby_blocks = list(block for block in nearby_blocks if block.item is None)
        return empty_nearby_blocks
