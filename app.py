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

@app.route("/initialize")
def initialize():
    if not all(map(lambda v: v in request.args, ('x', 'y', 'char'))):
        return jsonify({'error': 'x, y, and char fields are all required'}), 400
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
