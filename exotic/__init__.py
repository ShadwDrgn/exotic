from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import secrets


# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.sqlite3'

    # set secret key from file
    with open('flask.secret', 'a+') as f:
        f.seek(0)
        secret = f.read().strip()
        print(f'The secret is: {secret}', flush=True)
        if secret == '':
            secret = secrets.token_hex(nbytes=32)
            f.write(secret)
        app.secret_key = secret

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Include our Routes
        from exotic.routes import bp
        app.register_blueprint(bp)

        # Create the db
        db.create_all()

        return app
