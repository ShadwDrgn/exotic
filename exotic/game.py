import random
from exotic import db
class Game:
    characters = list()
    worlds = list()
    tick_rate = 15 # in seconds

    def last_tick():
        t = int(time.time())
        return t - t % Game.tick_rate

class Tile:
    def __init__(self, world, x, y, description='A Map Tile', tile_type='Forest'):
        self.world = world
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.description = description

    def __repr__(self):
        return f"{{'x': {self.x}, 'y': {self.y}, 'desc': {self.description}}}"

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
    
    def create(world_name, map_width, map_height):
        found_world = [w for w in Game.worlds if w.name == world_name]
        if len(found_world) > 0:
            return found_world[0]
        world = World(world_name, map_width, map_height)
        Game.worlds.append(world)
        return world


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


class Character(Mobile, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    world = db.Column(db.String, nullable=False)

    def __init__(self, owner, name, world, x, y):
        self.seen = 0
        self.action_points = 0
        self.base_action_points = 50
        self.owner = owner
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
        return Character.query.filter_by(name=character_name).first()

    def create(current_user, character_name, world_name, x, y):
        found_character = [c for c in Game.characters if c.name == character_name]
        if len(found_character) > 0:
            raise Exception('Character exists')
        worlds = [w for w in Game.worlds if w.name == world_name]
        if len(worlds) == 0:
            raise Exception('No such world')
        world = worlds[0]
        owner = int(current_user.id)
        character = Character(owner=owner, name=character_name, world=world.name, x=int(x), y=int(y))
        # Game.characters.append(character)
        db.session.add(character)
        db.session.commit()
        return character
