from map import *


class Object:
    objects = []

    def __init__(self, x, y, tag, _id):
        Object.objects.append(self)
        self.x, self.y = x, y
        self.tag, self.id = tag, _id
        self.declare_to_enter()

    def act(self):
        self.declare_to_leave()
        self.declare_to_enter()

    def get_available_directions(self):
        available_directions = [2, 4, 6, 8]
        x, y = self.x, self.y
        if y == 0 or not Map.blocks[x][y-1].is_accessible():
            # print("由于", " y == 0" if y == 0 else "地块 (%d, %d) 被占用" % (x, y-1), sep='')
            available_directions.remove(2)
            # print("方向2被移除")
        if x == 0 or not Map.blocks[x-1][y].is_accessible():
            # print("由于", " x == 0" if x == 0 else "地块 (%d, %d) 被占用" % (x-1, y), sep='')
            available_directions.remove(4)
            # print("方向4被移除")
        if x == MAP_WIDTH-1 or not Map.blocks[x+1][y].is_accessible():
            # print("由于", " x == MAP_WIDTH-1" if x == MAP_WIDTH-1 else "地块 (%d, %d) 被占用" % (x+1, y), sep='')
            available_directions.remove(6)
            # print("方向6被移除")
        if y == MAP_HEIGHT-1 or not Map.blocks[x][y+1].is_accessible():
            # print("由于", " y == MAP_HEIGHT-1" if y == MAP_HEIGHT-1 else "地块 (%d, %d) 被占用" % (x, y+1), sep='')
            available_directions.remove(8)
            # print("方向8被移除")
        return available_directions

    def move_towards(self, direction):
        self.x, self.y = Map.position_after_moving_towards((self.x, self.y), direction)

    def declare_to_leave(self):
        Map.blocks[self.x][self.y].lost(self)

    def declare_to_enter(self):
        Map.blocks[self.x][self.y].got(self)

    @staticmethod
    def get_rgb():
        raise RuntimeError

    def distance_with(self, obj):
        return abs(self.x - obj.x) + abs(self.y - obj.y)

    def full_name(self):
        return "%d 号%s" % (self.id, self.tag)


class Obstacle(Object):
    @staticmethod
    def get_rgb():
        return BLOCK_EDGE_RGB


class Food(Object):
    foods = []
    next_id = 1
    tag = "食物"

    def __init__(self, x, y):
        Object.__init__(self, x, y, Food.tag, Food.next_id)
        Food.foods.append(self)
        Food.next_id += 1

    @staticmethod
    def gen_random_food():
        while len(Food.foods) < FOOD_NUMBER:
            x, y = Map.get_accessible_position()
            Food(x, y)

    @staticmethod
    def get_rgb():
        return FOOD_RGB

    def eaten_by(self, obj):
        self.declare_to_leave()
        Food.foods.remove(self)
        Object.objects.remove(self)


class Ant(Object):
    ant_number = 0
    next_id = 1
    tag = "蚂蚁"

    def __init__(self, x, y, camp):
        Object.__init__(self, x, y, Ant.tag, Ant.next_id)
        self.camp = camp
        Ant.ant_number += 1
        Ant.next_id += 1

    def act(self):
        self.declare_to_leave()
        food = self.get_nearest_food()
        if food is None:
            direction = 0
        else:
            distance = self.distance_with(food)
            if distance == 1:
                self.eat(food)
                direction = 0
            else:
                possibility_to_reach_food = 1/distance * REACHING_FOOD_CORRECTION_FACTOR
                if random() <= possibility_to_reach_food:
                    direction = Map.direction_from_to((self.x, self.y), (food.x, food.y))
                    next_x, next_y = Map.position_after_moving_towards((self.x, self.y), direction)
                    if not Map.blocks[next_x][next_y].is_accessible():
                        direction = 0
                else:
                    direction = 0
        if direction == 0:
            available_directions = self.get_available_directions()
            if len(available_directions):
                direction = choice(available_directions)
            else:
                direction = 5
        self.move_towards(direction)
        self.declare_to_enter()

    def eat(self, food):
        x, y = food.x, food.y
        food.eaten_by(self)
        Ant(x, y, self.camp)

    def get_nearest_food(self):
        food = None
        distance = MAP_HEIGHT+MAP_WIDTH
        for f in Food.foods:
            d = self.distance_with(f)
            if d < distance or d == distance and randint(0, 1):
                food = f
                distance = d
        return food

    def get_rgb(self):
        return self.camp.get_rgb()
