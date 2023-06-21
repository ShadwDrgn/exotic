from exotic import init_app
from exotic.game import World

app = init_app()


if __name__ == "__main__":
    World.create('Prime', 100, 100)
    app.run(host='0.0.0.0')
