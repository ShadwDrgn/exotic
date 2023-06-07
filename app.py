from classes import *
from flask import Flask, current_app, jsonify, request, abort
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'giant stupid string that is definitely at total secret!!'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {
    'ShadwDrgn': {'password': 'pbkdf2:sha256:600000$OtUeSwJ3spOhzAjf$fda51497ebebb9b82914332c8bd22aaffb9f536565201f212af1ae8848a7caa1'}
}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form action='login' method='POST'>
            <input type='text' name='username' id='username' placeholder='username'/>
            <input type='password' name='password' id='password' placeholder='password'/>
            <input type='submit' name='submit'/>
            </form>
            '''
    username = request.form['username']
    if username in users and check_password_hash(users[username]['password'], request.form['password']):
        user = User()
        user.id = username
        flask_login.login_user(user)
        return jsonify({'message': 'logged in successfully'})
    return jsonify({'error': 'Bad Login'}), 401

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '''
            <form action='register' method='POST'>
            <input type='text' name='username' id='username' placeholder='username'/>
            <input type='password' name='password' id='password' placeholder='password'/>
            <input type='submit' name='submit'/>
            </form>
            '''
    username = request.form['username']
    password_hash = generate_password_hash(request.form['password'])
    if username in users:
        return jsonify({'error': 'User already exists'}), 400
    users[username] = {'password': password_hash}
    return jsonify({'message': 'User registered successfully'})


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
