from flask.ext.script import Server, Manager, Shell
from config import Config
from app import app

manager = Manager(app)

from views.index import bp as index_bp
app.register_blueprint(index_bp)

from models.dummy import Dummy


if __name__ == '__main__':
    manager.run()
