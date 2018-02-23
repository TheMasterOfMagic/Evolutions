from preparations import *
import math


class Object:
    objects = []
    id = None
    tag = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        Object.objects.append(self)

    def get_pos(self):
        return self.x, self.y

    def declare_to_enter(self):
        # print("%s即将进入地格%s" % (self.full_name(), self.get_pos()))
        Map.block((self.x, self.y)).got_obj(self)
        # print("%s已经进入地格%s" % (self.full_name(), self.get_pos()))

    def declare_to_leave(self):
        # print("%s即将离开地格%s" % (self.full_name(), self.get_pos()))
        Map.block((self.x, self.y)).lost_obj(self)
        # print("%s已经离开地格%s" % (self.full_name(), self.get_pos()))

    def act(self):
        pass

    def full_name(self):
        return "%d号%s" % (self.id, self.tag)


class Obstacle(Object):
    obstacles = []
    next_id = 1
    tag = "障碍"

    def __init__(self, x, y):
        Object.__init__(self, x, y)
        Obstacle.objects.append(self)
        self.id = Obstacle.next_id
        Obstacle.next_id += 1
        self.declare_to_enter()

    @staticmethod
    def get_rgb():
        return BLOCK_EDGE_RGB


class Ant(Object):
    ants = []
    next_id = 1
    tag = "蚂蚁"

    def __init__(self, x, y, camp: Camp):
        Object.__init__(self, x, y)
        Ant.ants.append(self)
        self.id = Ant.next_id
        Ant.next_id += 1
        self.camp = camp
        self.camp.ant_number += 1
        self.declare_to_enter()

    def get_rgb(self):
        return self.camp.get_rgb()

    def got(self, food):
        x, y = food.get_pos()
        food.disappear()
        self.camp.food_number += 1
        if self.camp.food_number == 5:
            Ant(x, y, self.camp)
            self.camp.food_number = 0

    def act(self):
        def log(*args, **kwargs):
            if debug:
                print(*args, **kwargs)
        debug = 0
        block = Map.block(self.get_pos())
        block.odor = max(0, block.odor-50)

        self.declare_to_leave()
        direction = 0
        neighbour_positions = Map.get_neighbours_of_position(self.get_pos())
        neighbour_blocks = list(Map.block(pos) for pos in neighbour_positions)
        accessible_neighbour_blocks = []
        for block in neighbour_blocks:
            if block.is_accessible() and not isinstance(block.obj, Ant):
                accessible_neighbour_blocks.append(block)
            elif isinstance(block.obj, Ant) and block.obj.camp != self.camp:
                # block.obj.got_killed()
                # self.got_killed()
                direction = 0

        if direction == 0 and len(accessible_neighbour_blocks):
            shuffle(accessible_neighbour_blocks)
            accessible_neighbour_blocks.sort(key=lambda block: block.odor, reverse=True)
            direction = Map.get_direction_to_neighbour(self.get_pos(), accessible_neighbour_blocks[0].get_pos())

            obj = Map.block(Map.get_position_after_moving_towards_direction(self.get_pos(), direction)).obj
            if isinstance(obj, Food):
                direction = 5
                self.got(obj)

        if direction == 0:
            log("无选中方向，开始在可行方向中随机选取")
            neighbours = Map.get_neighbours_of_position((self.x, self.y))
            log("获取到当前位置的相邻位置有 :", neighbours)
            empty_neighbours = list(neighbour for neighbour in neighbours
                                    if Map.block(neighbour).is_empty())
            log("其中为空的有 :", empty_neighbours)
            accessible_directions = list(Map.get_direction_to_neighbour((self.x, self.y), neighbour)
                                         for neighbour in empty_neighbours)
            log("所以可行的方向有 :", accessible_directions)
            direction = choice(accessible_directions) if len(accessible_directions) else 5
            log("随机选取方向 :", direction)
        self.move_towards(direction)

        log(self.full_name(), "准备进入", (self.x, self.y))
        self.declare_to_enter()
        log(self.full_name(), "已经进入", (self.x, self.y))

    def got_killed(self):
        self.camp.ant_number -= 1
        self.declare_to_leave()
        Ant.ants.remove(self)
        Object.objects.remove(self)

    def move_towards(self, direction):
        self.x, self.y = Map.get_position_after_moving_towards_direction((self.x, self.y), direction)


class Food(Object):
    foods = []
    next_id = 1
    tag = "食物"

    @staticmethod
    def get_sin_number_generator():
        pi = 3.1415926535
        a = 0.05
        omega = 0.04*pi
        phi = random()*2*pi
        b = 1
        x = 0
        while True:
            yield a*math.sin(omega*x+phi)+b
            x += 1

    def __init__(self, x, y):
        Object.__init__(self, x, y)
        Food.foods.append(self)
        self.id = Food.next_id
        Food.next_id += 1
        self.declare_to_enter()
        self.sin_number_generator = Food.get_sin_number_generator()

    @staticmethod
    def get_rgb():
        return 0, 255, 0

    @staticmethod
    def gen_food():
        while len(Food.foods) < FOOD_NUMBER:
            x, y = Map.get_random_empty_positions(1)[0]
            Food(x, y)

    def disappear(self):
        self.declare_to_leave()
        Food.foods.remove(self)
        Object.objects.remove(self)

    def act(self):
        Map.block(self.get_pos()).odor = FOOD_ORIGIN_QUALITY * next(self.sin_number_generator)


class Block:
    def __init__(self, x, y, obj=None):
        self.x, self.y = x, y
        self.obj = obj
        self.odor = 0
        self.odor_inc = 0
        self.accessible_neighbours = []

    def get_pos(self):
        return self.x, self.y

    def got_obj(self, obj: Object):
        self.obj = obj
        Map.set_position_empty((self.x, self.y), False)
        if isinstance(obj, Obstacle):
            Map.set_position_accessible((self.x, self.y), False)

    def lost_obj(self, obj: Object):
        self.obj = None
        Map.set_position_empty((self.x, self.y), True)
        if isinstance(obj, Obstacle):
            Map.set_position_accessible((self.x, self.y), True)

    def is_accessible(self):
        return not isinstance(self.obj, Obstacle)

    def is_empty(self):
        return self.obj is None

    def odor_out(self):
        self.odor *= 0.9
        if self.odor < 1:
            self.odor = 0
        max_float_factor = 0.95
        neighbour_blocks = list(Map.block(pos) for pos in Map.get_neighbours_of_position(self.get_pos()))
        accessible_neighbour_blocks = list(block for block in neighbour_blocks if block.is_accessible())
        accessible_neighbour_blocks.sort(key=lambda block: block.odor, reverse=True)
        if len(accessible_neighbour_blocks):
            block = accessible_neighbour_blocks[0]
            if self.odor < block.odor*max_float_factor:
                self.odor_inc += (block.odor*max_float_factor - self.odor) * 0.7

    def odor_in(self):
        self.odor += self.odor_inc
        self.odor_inc = 0

    def render(self):
        edge_width = 0 if self.obj is not None else BLOCK_EDGE_WIDTH
        rgb = BLOCK_EDGE_RGB if self.obj is None else self.obj.get_rgb()
        pygame.draw.rect(DISPLAYSURFACE, rgb,
                         pygame.Rect((MAP_BLOCK_X+self.x)*BLOCK_SIZE, (MAP_BLOCK_Y+self.y)*BLOCK_SIZE,
                                     BLOCK_SIZE, BLOCK_SIZE), edge_width)

        if self.is_empty():
            odor = self.odor
            rect_size = self.odor*BLOCK_SIZE//FOOD_ORIGIN_QUALITY  # f(FOOD_ORIGIN_QUALITY) = BLOCK_SIZE, f(0)=0
            rect_size = min(BLOCK_SIZE - 2, rect_size)
            edge_width = (BLOCK_SIZE-rect_size)//2
            r = 0
            g = min(1, self.odor/FOOD_ORIGIN_QUALITY)*192//1
            b = r
            rect = pygame.Rect((MAP_BLOCK_X+self.x)*BLOCK_SIZE+edge_width,
                               (MAP_BLOCK_Y+self.y)*BLOCK_SIZE+edge_width,
                               BLOCK_SIZE-2*edge_width,
                               BLOCK_SIZE-2*edge_width)
            try:
                pygame.draw.rect(DISPLAYSURFACE, (r, g, b), rect, 0)
            except TypeError:
                print("g =", g)
                exit(1)


class Map:
    __blocks = None
    __empty_positions = None
    __accessible_positions = None

    @staticmethod
    def init():
        Map.__blocks = list()
        Map.__empty_positions = set()
        Map.__accessible_positions = set()
        Map.__p2p_directions = dict()
        Map.__p2p_distances = dict()

        for x in range(MAP_WIDTH):
            Map.__blocks.append(list())
            for y in range(MAP_HEIGHT):
                Map.__blocks[x].append(Block(x, y))
                Map.set_position_empty((x, y), True)
                Map.set_position_accessible((x, y), True)

    @staticmethod
    def calc_accessible_neighbours():
        for pos in Map.__accessible_positions:
            neighbours = Map.get_neighbours_of_position(pos)
            accessible_neighbours = list(neighbour for neighbour in neighbours
                                         if Map.block(neighbour).is_accessible())
            Map.block(pos).accessible_neighbours = list(Map.block(neighbour) for neighbour in accessible_neighbours)

    @staticmethod
    def get_random_empty_positions(n=1):
        try:
            return sample(Map.__empty_positions, n)
        except ValueError:
            raise GameOverException

    @staticmethod
    def block(pos: tuple([int, int])) -> Block:
        x, y = pos
        return Map.__blocks[x][y]

    @staticmethod
    def block_give_odor():
        for pos in Map.__accessible_positions:
            Map.block(pos).odor_out()

    @staticmethod
    def block_receive_odor():
        for pos in Map.__accessible_positions:
            Map.block(pos).odor_in()

    @staticmethod
    def set_position_empty(pos: tuple([int, int]), empty: bool):
        x, y = pos
        if empty:
            Map.__empty_positions.add((x, y))
        else:
            Map.__empty_positions.remove((x, y))

    @staticmethod
    def set_position_accessible(pos: tuple([int, int]), accessible: bool):
        x, y = pos
        if accessible:
            Map.__accessible_positions.add((x, y))
        else:
            Map.__accessible_positions.remove((x, y))

    @staticmethod
    def render():
        for block_line in Map.__blocks:
            for block in block_line:
                block.render()

    @staticmethod
    def gen_obstacles():
        if OBSTACLE_TYPE == "salt":
            Map.__gen_salt_obstacles()
        else:
            raise ValueError("Unrecognized obstacles' type : %s" % OBSTACLE_TYPE)

    @staticmethod
    def __gen_salt_obstacles():
        def log(*args, **kwargs):
            if debug:
                print(*args, **kwargs)
        debug = 0
        log("准备生成椒盐式障碍物")
        factor = OBSTACLE_FACTOR
        if 0 <= factor < 1:
            factor = int(MAP_WIDTH*MAP_HEIGHT*factor)
        if factor >= MAP_WIDTH*MAP_HEIGHT:
            raise ValueError("Too many obstacles")
        log("待生成数目 :", factor)
        positions = Map.get_random_empty_positions(factor)
        log("获取到如下", factor, "个随机空位置 :", positions)
        for position in positions:
            x, y = position
            Obstacle(x, y)

    @staticmethod
    def manhattan_distance(pos1, pos2):
        (x1, y1), (x2, y2) = pos1, pos2
        return abs(x2-x1)+abs(y2-y1)

    @staticmethod
    def get_neighbours_of_position(pos):
        neighbours = []
        x, y = pos
        if y > 0:
            neighbours.append((x, y-1))
        if x > 0:
            neighbours.append((x-1, y))
        if x < MAP_WIDTH - 1:
            neighbours.append((x+1, y))
        if y < MAP_HEIGHT - 1:
            neighbours.append((x, y+1))
        return neighbours

    @staticmethod
    def get_direction_to_neighbour(pos, neighbour):
        if Map.manhattan_distance(pos, neighbour) != 1:
            raise ValueError("%s is not neighbour of %s" % (str(pos), str(neighbour)))
        (x1, y1), (x2, y2) = pos, neighbour
        vertical = 4 if x2 < x1 else 0 if x2 == x1 else 6
        horizontal = 2 if y2 < y1 else 0 if y2 == y1 else 8
        return vertical + horizontal

    @staticmethod
    def get_position_after_moving_towards_direction(start, direction):
        x, y = start
        x += -1 if direction == 4 else 1 if direction == 6 else 0
        y += -1 if direction == 2 else 1 if direction == 8 else 0
        if direction not in (2, 4, 5, 6, 8):
            raise ValueError("Illegal direction : %d" % direction)
        return x, y

    @staticmethod
    def get_p2p_direction_and_distance(pos1, pos2, max_searching_distance=INFINITE_DISTANCE):
        if pos1 == pos2:
            return 5, 0
        start, end = pos1, pos2
        open_list = [start]
        close_list = set()
        prev_list = {start: None}
        g_list = {start: 0}

        while len(open_list):
            current = open_list.pop(0)
            if g_list[current] == max_searching_distance:
                end = current
            if current == end:
                break
            close_list.add(current)
            neighbours = Map.get_neighbours_of_position(current)
            neighbours = list(neighbour for neighbour in neighbours
                              if neighbour == end or Map.block(neighbour).is_empty())
            for position in neighbours:
                if position in close_list:
                    continue
                if position not in open_list:
                    open_list.append(position)
                    prev_list[position] = current
                    g_list[position] = g_list[current] + 1
                else:
                    gp, gc = g_list[position], g_list[current]
                    if gp > gc + 1 or gp == gc + 1 and randint(0, 1):
                        prev_list[position] = current
                        g_list[position] = gc + 1
            open_list.sort(key=lambda pos: g_list[pos]+Map.manhattan_distance(pos, end))
        # end while

        direction, distance = 0, INFINITE_DISTANCE
        if end in prev_list:
            distance = 1
            current = end
            while prev_list[current] != start:
                current = prev_list[current]
                distance += 1
            direction = Map.get_direction_to_neighbour(start, current)
        return direction, distance


Map.init()
