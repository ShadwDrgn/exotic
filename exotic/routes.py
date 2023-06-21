from exotic import login_manager
from exotic import db
from exotic.game import Character, World, Game
from exotic.account_management import User
from flask import Flask, current_app, jsonify, request, abort, session, Blueprint
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

bp = Blueprint('bp', __name__)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@bp.route("/login", methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    # Use a User.login method instead of all this
    users = User.query.filter_by(username=username)
    user =  users.first()
    if user is None or not check_password_hash(user.password_hash, password):
        logout_user(user)
        return jsonify({'error': 'Bad Login'}), 401
    login_user(user)
    return gamestate()
    

@bp.route("/logout")
def logout():
    logout_user()
    session.clear()
    return jsonify({'message': 'User Logged out'})

@bp.route("/register", methods=['POST'])
def register():
    username = request.get_json()['username']
    password = request.get_json()['password']
    # Use a User.register method instead of all this
    password_hash = generate_password_hash(password)
    if User.query.filter_by(username=username).count() >= 1:
        return jsonify({'error': 'User already exists'}), 400
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@bp.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

# Remove this (Use a gamestate method on Character)
@bp.route("/tiles")
def tiles():
    if 'active_character' not in session:
        return jsonify({'error': 'Character invalid'}), 400
    current_character = Character.load(session['active_character'])
    worlds = [world for world in Game.worlds if world.name == current_character.world]
    world = worlds[0]
    tiles = [t.toJSON() for t in world.tiles if abs(t.x - current_character.x) <= 2 and abs(t.y - current_character.y) <=2]
    return jsonify(tiles)

@bp.route("/active_character", methods=['POST'])
def active_character():
    data = request.get_json()
    character_name = data['charname']
    session['active_character'] = character_name
    return gamestate()

# This entire endpoint should be behind an admin page
@bp.route("/create_world")
def create_world():
    try:
        world = World.create('Prime', 100, 100)
        return jsonify({'worlds': [world.name for world in Game.worlds] })
    except Exception as e:
        return jsonify({'error': str(e) })
        

@bp.route("/create_character", methods=['POST'])
def create_character():
    data = request.get_json()
    character_name = data['charname']
    x = 3
    y = 3
    character = Character.create(current_user, character_name, 'Prime', x, y)
    session['active_character'] = character_name
    return gamestate()

@bp.route('/gamestate')
def gamestate():
    if (isinstance(current_user, AnonymousUserMixin)):
        return jsonify({'current_user': None})
    return jsonify({'current_user': { 'id': current_user.username, 'characters': current_user.characters } })


@bp.route('/move')
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
    db.session.commit()
    return tiles()

@bp.route("/")
def hello():
    return current_app.send_static_file('map.html')
    # return "Hello World!"
