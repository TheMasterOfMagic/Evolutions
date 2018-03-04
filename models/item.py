from random import sample


class Item:
    __items = set()

    def __init__(self, block):
        self.block = None
        self.enter_block(block)
        self.to_be_cleared = False
        Item.__items.add(self)

    def leave_block(self):
        self.block.lost_item()
        self.block = None

    def enter_block(self, block):
        self.block = block
        self.block.got_item(self)

    @staticmethod
    def get_color():
        return None

    @staticmethod
    def act():
        pass

    @classmethod
    def items_act(cls):
        for item in cls.__items.copy():
            item.act()

    @classmethod
    def lost_item(cls, item):
        cls.__items.remove(item)


class Obstacle(Item):
    __obstacles = set()
    tag = "obstacle"

    def __init__(self, block):
        Item.__init__(self, block)
        Obstacle.__obstacles.add(self)


class Food(Item):
    __foods = set()
    tag = "food"

    def __init__(self, block):
        Item.__init__(self, block)
        Food.__foods.add(self)

    def got_eaten(self):
        self.leave_block()
        Food.__foods.remove(self)
        Item.lost_item(self)

    def act(self):
        if self.block:
            self.block.odors[Food] = 1000

    @classmethod
    def get_food_number(cls):
        return len(cls.__foods)


class Ant(Item):
    __ants = set()
    tag = "ant"

    def __init__(self, block, camp):
        Item.__init__(self, block)
        self.camp = camp
        Ant.__ants.add(self)

    def act(self):
        if self.block:
            self.block.odors[self.camp] = 1000
            nearby_blocks = self.block.get_nearby_blocks()
            for block in nearby_blocks:
                if block.item and block.item.tag is "food":
                    block.item.got_eaten()
                    self.leave_block()
                    self.enter_block(block)
                    return
            empty_nearby_blocks = self.block.get_empty_nearby_blocks()
            target_nearby_block = max(empty_nearby_blocks, key=lambda x: x.odors[Food])
            self.leave_block()
            self.enter_block(target_nearby_block)
