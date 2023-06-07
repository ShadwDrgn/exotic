from classes import *
from flask import Flask, current_app, jsonify, request, abort
app = Flask(__name__)

@app.route("/tiles")
def tiles():
    current_character = Character.load(request.args.get('char'))
    if current_character is None:
        return jsonify({'error': 'Character invalid'}), 400
    tiles = [t.toJSON() for t in current_character.world.tiles if abs(t.x - current_character.x) <= 2 and abs(t.y - current_character.y) <=2]
    return jsonify(tiles)

@app.route("/create_world")
def create_world():
    try:
        world = World.create('Prime', 100, 100)
        return jsonify({'worlds': [world.name for world in Game.worlds] })
    except Exception as e:
        print(e.__traceback__, flush=True)
        return jsonify({'error': str(e) })
        

@app.route("/create_character")
def create_character():
    if not all(map(lambda param: param in request.args, ('name', 'x', 'y'))):
        return jsonify({'error': 'name, x, and y are required fields' })
    try:
        character_name = request.args.get('name')
        x = request.args.get('x')
        y = request.args.get('y')
        character = Character.create(character_name, 'Prime', x, y)
        return jsonify({'Characters': [character.name for character in Game.characters] })
    except Exception as e:
        return jsonify({'error': str(e) })


@app.route('/move')
def move():
    x, y = int(request.args.get('x')), int(request.args.get('y'))
    current_character = Character.load(request.args.get('char'))
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
