from flask import Flask
from flask_restful import Api
from flask.ext.assets import Environment, Bundle
from webassets.filter import register_filter
from webassets_browserify import Browserify
from flask_sqlalchemy import SQLAlchemy
from config import Config


register_filter(Browserify)

DB = SQLAlchemy()
API = Api()
ASSETS = Environment()

SCSS = Bundle('scss/*.scss', 'scss/components/*.scss', filters='scss', output='gen/app.css')
JSX = Bundle('jsx/*.jsx', filters='browserify', output='gen/app.js')

ASSETS.register('scss', SCSS)
ASSETS.register('jsx', JSX)

def create_app():
    """ Initializing the app """
    app = Flask(__name__)
    app.config.update(Config.__dict__)

    # Set up extensions
    DB.init_app(app)
    app.DB = DB

    API.init_app(app)
    ASSETS.init_app(app)

    # Install views
    from views.index import bp as index_bp
    app.register_blueprint(index_bp)

    # Install models
    from models.account import User

    with app.app_context():
        DB.create_all()

    return app
