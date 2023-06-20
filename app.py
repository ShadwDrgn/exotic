from classes import Character, World, Game
from account_management import User
from flask import Flask, current_app, jsonify, request, abort, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)

with open('flask.secret', 'w+') as f:
    secret = f.read().strip()
    if secret == '':
        secret = secrets.token_hex(nbytes=32)
        f.write(secret)
    app.secret_key = secret
        
    
login_manager = LoginManager()
login_manager.init_app(app)

users = dict()

World.create('Prime', 100, 100)

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@app.route("/login", methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    # Use a User.login method instead of all this
    if username in users and check_password_hash(users[username]['password'], password):
        user = User()
        user.id = username
        login_user(user)
        return gamestate()
    logout_user()
    return jsonify({'error': 'Bad Login'}), 401

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return jsonify({'message': 'User Logged out'})

@app.route("/register", methods=['POST'])
def register():
    username = request.get_json()['username']
    password = request.get_json()['password']
    # Use a User.register method instead of all this
    password_hash = generate_password_hash(password)
    if username in users:
        return jsonify({'error': 'User already exists'}), 400
    users[username] = {'password': password_hash}
    return jsonify({'message': 'User registered successfully'})

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

# Remove this (Use a gamestate method on Character)
@app.route("/tiles")
def tiles():
    if 'active_character' not in session:
        return jsonify({'error': 'Character invalid'}), 400
    print('********************************GOT HERE********************************', flush=True)
    current_character = Character.load(session['active_character'])
    print(session['active_character'], flush=True)
    tiles = [t.toJSON() for t in current_character.world.tiles if abs(t.x - current_character.x) <= 2 and abs(t.y - current_character.y) <=2]
    return jsonify(tiles)

@app.route("/active_character", methods=['POST'])
def active_character():
    data = request.get_json()
    character_name = data['charname']
    session['active_character'] = character_name
    return gamestate()

# This entire endpoint should be behind an admin page
@app.route("/create_world")
def create_world():
    try:
        world = World.create('Prime', 100, 100)
        return jsonify({'worlds': [world.name for world in Game.worlds] })
    except Exception as e:
        print(e.__traceback__, flush=True)
        return jsonify({'error': str(e) })
        

@app.route("/create_character", methods=['POST'])
def create_character():
    data = request.get_json()
    character_name = data['charname']
    x = 3
    y = 3
    character = Character.create(current_user, character_name, 'Prime', x, y)
    session['active_character'] = character_name
    return gamestate()

@app.route('/gamestate')
def gamestate():
    if (isinstance(current_user, AnonymousUserMixin)):
        return jsonify({'current_user': None})
    current_user.characters = [c.name for c in Game.characters if c.owner == current_user.id]
    return jsonify({'current_user': { 'id': current_user.id, 'characters': current_user.characters } })


@app.route('/move')
def move():
    # Use Character.move method instead of all this
    if 'active_character' not in session:
        return jsonify({'error': 'Character invalid'}), 400
    x, y = int(request.args.get('x')), int(request.args.get('y'))
    current_character = Character.load(session['active_character'])
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
