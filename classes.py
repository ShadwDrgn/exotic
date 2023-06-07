import random
class Game:
    characters = list()
    worlds = list()
    tick_rate = 15 # in seconds
    def last_tick():
        t = int(time.time())
        return t - t % Game.tick_rate
    def get_character(name):
        found = [c for c in Game.characters if c.name == name]
        if len(found) > 0:
            return found[0]
        return None

class Tile:
    def __init__(self, world, x, y, description='A Map Tile', tile_type='Forest'):
        self.world = world
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.description = description

    def __repr__(self):
        return {'x': self.x, 'y': self.y, 'desc': self.description}

    def toJSON(self):
        return {'x': self.x, 'y': self.y, 'desc': self.description, 'tile_type': self.tile_type}


    def characters(self):
        return [c for c in Game.characters if c.position() == (self.world, self.x, self.y)]


class World:
    def __init__(self, name, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tiles = list()
        self.name = name
        for x in range(map_width):
            for y in range(map_height):
                tile_type = random.choice(['forest', 'grass', 'industrial', 'commercial'])
                if tile_type == 'forest':
                        desc = 'A desolate forest'
                if tile_type == 'grass':
                        desc = 'A field of grass'
                if tile_type == 'industrial':
                        desc = random.choice(['A factory', 'A warehouse', 'A power plant'])
                if tile_type == 'commercial':
                        desc = random.choice(['A crappy taco restaurant', 'A tasty burger joint', 'A clothing store', 'A pet shop'])
                self.tiles.append(Tile(self, x, y, desc, tile_type))

    def characters(self):
        return [c for c in Game.characters if c.world == self]


class Mobile:
    def __init__(self, name, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return self.name
    
    def position():
        return (self.world, self.x, self.y)

    def generate():
        #name = ''.join([random.choice(string.ascii_letters) for i in range(8)])
        name = random.choice(names)
        x = random.randint(0,24)
        y = random.randint(0,24)
        return Mobile(name, x, y)


class Character(Mobile):
    def __init__(self, name, world, x, y):
        self.seen = 0
        self.action_points = 0
        self.base_action_points = 50
        super().__init__(name, world, x, y)

    def update(self):
        # The last time the player was given AP
        last_action_point = self.seen - self.seen % Game.tick_rate
        # The amount of AP they're about to have
        new_value = self.action_points + int((Game.last_tick() - last_action_point) / Game.tick_rate)
        # set it
        self.action_points = min(self.max_ap(), new_value)
        # set the seen time so we know they got ap.
        self.seen = int(time.time())
        # return the new ap value so the calling function knows stuff.
        return self.action_points

    def max_ap(self):
        return self.base_action_points

    def load(character_name):
        found_character = [c for c in Game.characters if c.name == character_name]
        if len(found_character) > 0:
            return found_character[0]
        return None