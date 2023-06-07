from classes import *
from flask import Flask, current_app, jsonify, request
app = Flask(__name__)

@app.route("/tiles")
def tiles():
    current_character = [c for c in Game.characters if c.name == request.args.get('char')]
    if len(current_character) > 0:
        current_character = current_character[0]
        print(current_character.x, flush=True)
        print(current_character.world.tiles[0].x, flush=True)
        tiles = [t.toJSON() for t in current_character.world.tiles if abs(t.x - current_character.x) <= 2 and abs(t.y - current_character.y) <=2]
        return jsonify(tiles)
    tile_data = [{'x': 1, 'y': 1, 'desc': 'Swamp'},
 {'x': 2, 'y': 1, 'desc': 'Forest'},
 {'x': 3, 'y': 1, 'desc': 'Taco stand'},
 {'x': 4, 'y': 1, 'desc': 'Swamp'},
 {'x': 5, 'y': 1, 'desc': 'Path'},
 {'x': 1, 'y': 2, 'desc': 'Swamp'},
 {'x': 2, 'y': 2, 'desc': 'Swamp'},
 {'x': 3, 'y': 2, 'desc': 'Forest'},
 {'x': 4, 'y': 2, 'desc': 'Island'},
 {'x': 5, 'y': 2, 'desc': 'Path'},
 {'x': 1, 'y': 3, 'desc': 'Taco stand'},
 {'x': 2, 'y': 3, 'desc': 'Forest'},
 {'x': 3, 'y': 3, 'desc': 'Path'},
 {'x': 4, 'y': 3, 'desc': 'Island'},
 {'x': 5, 'y': 3, 'desc': 'Swamp'},
 {'x': 1, 'y': 4, 'desc': 'Forest'},
 {'x': 2, 'y': 4, 'desc': 'Path'},
 {'x': 3, 'y': 4, 'desc': 'Island'},
 {'x': 4, 'y': 4, 'desc': 'Taco stand'},
 {'x': 5, 'y': 4, 'desc': 'Island'},
 {'x': 1, 'y': 5, 'desc': 'Island'},
 {'x': 2, 'y': 5, 'desc': 'Taco stand'},
 {'x': 3, 'y': 5, 'desc': 'Swamp'},
 {'x': 4, 'y': 5, 'desc': 'Taco stand'},
 {'x': 5, 'y': 5, 'desc': 'Path'}]
    return jsonify(tile_data)

@app.route("/initialize")
def initialize():
    if any(i.name == 'prime' for i in Game.worlds):
        prime = [w for w in Game.worlds if w.name == 'prime'][0]
    else:
        prime = World('prime', 100, 100)
        Game.worlds.append(prime)
    x, y = int(request.args.get('x')), int(request.args.get('y'))
    if not any(c.name == request.args.get('char') for c in Game.characters):
        c = Character(request.args.get('char'), prime, x, y)
        Game.characters.append(c)
    return jsonify({'status': 'ok', 'characters': [c.name for c in Game.characters], 'worlds': f'{len(Game.worlds)} Worlds' })
    

@app.route('/move')
def move():
    x, y = int(request.args.get('x')), int(request.args.get('y'))
    current_character = Game.get_character(request.args.get('char'))
    if current_character is None:
        abort(400, 'No such character')
    current_character.x = x
    current_character.y = y
    tiles = [t.toJSON() for t in current_character.world.tiles if abs(t.x - current_character.x) <= 2 and abs(t.y - current_character.y) <=2]
    return jsonify(tiles)

@app.route("/")
def hello():
    return current_app.send_static_file('map.html')
    # return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
