from preparations import *


if 0 <= OBSTACLE_NUMBER < 1:
    OBSTACLE_NUMBER = int(OBSTACLE_NUMBER*MAP_WIDTH*MAP_HEIGHT)
if OBSTACLE_NUMBER >= MAP_HEIGHT*MAP_WIDTH:
    raise RuntimeError


class Obstacle:
    @staticmethod
    def get_rgb():
        return BLOCK_EDGE_RGB


class Block:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.obj = None

    def got(self, obj):
        # print("地块", (self.x, self.y), "即将被", obj.full_name(), "占用")
        self.obj = obj
        Map.accessible_positions.remove((self.x, self.y))
        # print("地块", (self.x, self.y), "已经被", obj.full_name(), "占用")

    def lost(self, obj):
        # print("地块", (self.x, self.y), "即将被", obj.full_name(), "释放")
        self.obj = None
        Map.accessible_positions.append((self.x, self.y))
        # print("地块", (self.x, self.y), "已经被", obj.full_name(), "释放")

    def render(self):
        edge_width = 0 if self.obj is not None else BLOCK_EDGE_WIDTH
        rgb = BLOCK_EDGE_RGB if self.obj is None else self.obj.get_rgb()
        pygame.draw.rect(DISPLAYSURFACE, rgb,
                         pygame.Rect((MAP_BLOCK_X+self.x)*BLOCK_SIZE, (MAP_BLOCK_Y+self.y)*BLOCK_SIZE,
                                     BLOCK_SIZE, BLOCK_SIZE), edge_width)

    def is_accessible(self):
        # print("地块", (self.x, self.y), " ", "" if self.obj is None else "不", "可用", sep="")
        return self.obj is None


class Map:
    blocks = [[]]
    accessible_positions = []

    @staticmethod
    def init():
        Map.blocks = list(list(Block(x, y) for y in range(MAP_HEIGHT)) for x in range(MAP_WIDTH))
        Map.accessible_positions = list((x, y) for y in range(MAP_HEIGHT) for x in range(MAP_WIDTH))

    @staticmethod
    def render():
        for block_line in Map.blocks:
            for block in block_line:
                block.render()

    @staticmethod
    def get_accessible_position():
        if len(Map.accessible_positions):
            return choice(Map.accessible_positions)
        print("No accessible positions anymore\nGame Over")
        raise GameOverException

    @staticmethod
    def direction_from_to(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        left_or_right = 4 if x2 < x1 else 0 if x2 == x1 else 6
        up_or_down = 2 if y2 < y1 else 0 if y2 == y1 else 8
        if left_or_right and up_or_down:
            direction = left_or_right if randint(0, 1) else up_or_down
        else:
            direction = left_or_right + up_or_down
        return direction

    @staticmethod
    def position_after_moving_towards(start, direction):
        x, y = start
        if direction in (4, 6):
            x += -1 if direction == 4 else 1
        elif direction in (2, 8):
            y += -1 if direction == 2 else 1
        elif direction != 5:
            raise RuntimeError
        if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
            raise RuntimeError
        return x, y


Map.init()
